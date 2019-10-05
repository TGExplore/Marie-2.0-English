import json, time, os
from io import BytesIO
from typing import Optional

from telegram import MAX_MESSAGE_LENGTH, ParseMode, InlineKeyboardMarkup
from telegram import Message, Chat, Update, Bot
from telegram.error import BadRequest
from telegram.ext import CommandHandler, run_async, Filters

import tg_bot.modules.sql.notes_sql as sql
from tg_bot import dispatcher, LOGGER, OWNER_ID, SUDO_USERS, TEMPORARY_DATA
from tg_bot.__main__ import DATA_IMPORT
from tg_bot.modules.helper_funcs.chat_status import user_admin
from tg_bot.modules.helper_funcs.misc import build_keyboard, revert_buttons
from tg_bot.modules.helper_funcs.msg_types import get_note_type
from tg_bot.modules.rules import get_rules
from tg_bot.modules.helper_funcs.string_handling import button_markdown_parser, make_time

# SQL

from tg_bot.modules.sql import cust_filters_sql as filtersql
import tg_bot.modules.sql.locks_sql as locksql
from tg_bot.modules.locks import LOCK_TYPES, RESTRICTION_TYPES
from tg_bot.modules.sql import notes_sql as notesql
import tg_bot.modules.sql.rules_sql as rulessql
import tg_bot.modules.sql.welcome_sql as welcsql

from tg_bot.modules.connection import connected

from tg_bot.modules.helper_funcs.msg_types import Types

@run_async
@user_admin
def import_data(bot: Bot, update):
	msg = update.effective_message  # type: Optional[Message]
	chat = update.effective_chat  # type: Optional[Chat]
	user = update.effective_user  # type: Optional[User]
	# TODO: allow uploading doc with command, not just as reply

	conn = connected(bot, update, chat, user.id, need_admin=True)
	if conn:
		chat = dispatcher.bot.getChat(conn)
		chat_id = conn
		chat_name = dispatcher.bot.getChat(conn).title
	else:
		if update.effective_message.chat.type == "private":
			update.effective_message.reply_text(update.effective_message, "Anda bisa lakukan command ini pada grup, bukan pada PM")
			return ""
		chat = update.effective_chat
		chat_id = update.effective_chat.id
		chat_name = update.effective_message.chat.title

	if msg.reply_to_message and msg.reply_to_message.document:
		filetype = msg.reply_to_message.document.file_name
		if filetype.split('.')[-1] not in ("backup", "json", "txt"):
			msg.reply_text(tl(update.effective_message, "File cadangan tidak valid!"))
			return
		try:
			file_info = bot.get_file(msg.reply_to_message.document.file_id)
		except BadRequest:
			msg.reply_text(update.effective_message, "Coba unduh dan unggah ulang file seperti Anda sendiri sebelum mengimpor - yang ini sepertinya rusak!")
			return

		with BytesIO() as file:
			file_info.download(out=file)
			file.seek(0)
			data = json.load(file)

		try:
			# If backup is from Monica
			if data.get('bot_base') == "Monica":
				imp_filters_count = 0
				imp_greet = False
				imp_gdbye = False
				imp_greet_pref = False
				imp_locks = False
				imp_notes = 0
				imp_rules = False
				NOT_IMPORTED = "This cannot be imported because from other bot."
				NOT_IMPORTED_INT = 0
				# If backup is from this bot, import all files
				if data.get('bot_id') == bot.id:
					is_self = True
				else:
					is_self = False
				# Import filters
				if data.get('filters'):
					NOT_IMPORTED += "\n\nFilters:\n"
					for x in data['filters'].get('filters'):
						# If from self, import all
						if is_self:
							is_sticker = False
							is_document = False
							is_image = False
							is_audio = False
							is_voice = False
							is_video = False
							has_markdown = False
							universal = False
							if x['type'] == 1:
								is_sticker = True
							elif x['type'] == 2:
								is_document = True
							elif x['type'] == 3:
								is_image = True
							elif x['type'] == 4:
								is_audio = True
							elif x['type'] == 5:
								is_voice = True
							elif x['type'] == 6:
								is_video = True
							elif x['type'] == 0:
								has_markdown = True
							note_data, buttons = button_markdown_parser(x['reply'], entities=0)
							filtersql.add_filter(chat_id, x['name'], note_data, is_sticker, is_document, is_image, is_audio, is_voice, is_video, buttons)
							imp_filters_count += 1	
						else:
							if x['has_markdown']:
								note_data, buttons = button_markdown_parser(x['reply'], entities=0)
								filtersql.add_filter(chat_id, x['name'], note_data, False, False, False, False, False, False, buttons)
								imp_filters_count += 1
							else:
								NOT_IMPORTED += "- {}\n".format(x['name'])
								NOT_IMPORTED_INT += 1

				# Import greetings
				if data.get('greetings'):
					if data['greetings'].get('welcome'):
						welcenable = data['greetings']['welcome'].get('enable')
						welcsql.set_welc_preference(str(chat_id), bool(welcenable))

						welctext = data['greetings']['welcome'].get('text')
						welctype = data['greetings']['welcome'].get('type')
						if welctype == 0:
							welctype = Types.TEXT
						elif welctype == 1:
							welctype = Types.BUTTON_TEXT
						elif welctype == 2:
							welctype = Types.STICKER
						elif welctype == 3:
							welctype = Types.DOCUMENT
						elif welctype == 4:
							welctype = Types.PHOTO
						elif welctype == 5:
							welctype = Types.AUDIO
						elif welctype == 6:
							welctype = Types.VOICE
						elif welctype == 7:
							welctype = Types.VIDEO
						elif welctype == 8:
							welctype = Types.VIDEO_NOTE
						else:
							welctype = None
						welccontent = data['greetings']['welcome'].get('content')
						if welctext and welctype:
							note_data, buttons = button_markdown_parser(welctext, entities=0)
							welcsql.set_custom_welcome(chat_id, welccontent, note_data, welctype, buttons)
							imp_greet = True
					if data['greetings'].get('goodbye'):
						gdbyenable = data['greetings']['goodbye'].get('enable')
						welcsql.set_gdbye_preference(str(chat_id), bool(gdbyenable))

						gdbytext = data['greetings']['goodbye'].get('text')
						gdbytype = data['greetings']['goodbye'].get('type')
						if gdbytype == 0:
							gdbytype = Types.TEXT
						elif gdbytype == 1:
							gdbytype = Types.BUTTON_TEXT
						elif gdbytype == 2:
							gdbytype = Types.STICKER
						elif gdbytype == 3:
							gdbytype = Types.DOCUMENT
						elif gdbytype == 4:
							gdbytype = Types.PHOTO
						elif gdbytype == 5:
							gdbytype = Types.AUDIO
						elif gdbytype == 6:
							gdbytype = Types.VOICE
						elif gdbytype == 7:
							gdbytype = Types.VIDEO
						elif gdbytype == 8:
							gdbytype = Types.VIDEO_NOTE
						else:
							gdbytype = None
						gdbycontent = data['greetings']['goodbye'].get('content')
						if welctext and gdbytype:
							note_data, buttons = button_markdown_parser(gdbytext, entities=0)
							welcsql.set_custom_gdbye(chat_id, gdbycontent, note_data, gdbytype, buttons)
							imp_gdbye = True

				# clean service
				cleanserv = data['greetings'].get('clean_service')
				welcsql.set_clean_service(chat_id, bool(cleanserv))

				# security welcome
				if data['greetings'].get('security'):
					secenable = data['greetings']['security'].get('enable')
					secbtn = data['greetings']['security'].get('text')
					sectime = data['greetings']['security'].get('time')
					welcsql.set_welcome_security(chat_id, bool(secenable), str(sectime), str(secbtn))
					imp_greet_pref = True

				# Import Locks
				if data.get('locks'):
					if data['locks'].get('lock_warn'):
						locksql.set_lockconf(chat_id, True)
					else:
						locksql.set_lockconf(chat_id, False)
					if data['locks'].get('locks'):
						for x in list(data['locks'].get('locks')):
							if x in LOCK_TYPES:
								is_locked = data['locks']['locks'].get('x')
								locksql.update_lock(chat_id, x, locked=is_locked)
								imp_locks = True
							if x in RESTRICTION_TYPES:
								is_locked = data['locks']['locks'].get('x')
								locksql.update_restriction(chat_id, x, locked=is_locked)
								imp_locks = True

				# Import notes
				if data.get('notes'):
					allnotes = data['notes']
					NOT_IMPORTED += "\n\nNotes:\n"
					for x in allnotes:
						# If from self, import all
						if is_self:
							note_data, buttons = button_markdown_parser(x['note_data'], entities=0)
							note_name = x['note_tag']
							note_file = None
							note_type = x['note_type']
							if x['note_file']:
								note_file = x['note_file']
							if note_type == 0:
								note_type = Types.TEXT
							elif note_type == 1:
								note_type = Types.BUTTON_TEXT
							elif note_type == 2:
								note_type = Types.STICKER
							elif note_type == 3:
								note_type = Types.DOCUMENT
							elif note_type == 4:
								note_type = Types.PHOTO
							elif note_type == 5:
								note_type = Types.AUDIO
							elif note_type == 6:
								note_type = Types.VOICE
							elif note_type == 7:
								note_type = Types.VIDEO
							elif note_type == 8:
								note_type = Types.VIDEO_NOTE
							else:
								note_type = None
							if note_type <= 8:
								notesql.add_note_to_db(chat_id, note_name, note_data, note_type, buttons, note_file)
								imp_notes += 1
						else:
							# If this text
							if x['note_type'] == 0:
								note_data, buttons = button_markdown_parser(x['text'].replace("\\", ""), entities=0)
								note_name = x['name']
								notesql.add_note_to_db(chat_id, note_name, note_data, Types.TEXT, buttons, None)
								imp_notes += 1
							else:
								NOT_IMPORTED += "- {}\n".format(x['name'])
								NOT_IMPORTED_INT += 1

				# Import rules
				if data.get('rules'):
					contrules = data['rules'].get('rules')
					if contrules:
						rulessql.set_rules(chat_id, contrules)
						imp_rules = True

				if conn:
					text = (update.effective_message, "Full backup returned on *{}*. Welcome backup! ").format(chat_name)
				else:
					text = (update.effective_message, "Backup fully restored.\nDone with welcome backup! ").format(chat_name)
				text += (update.effective_message, "\n\n I've returned it:\n")
				if imp_filters_count:
					text += (update.effective_message, "- {} filters\n").format(imp_filters_count)
				if imp_greet_pref:
					text += (update.effective_message, "- Greeting settings\n")
				if imp_greet:
					text += (update.effective_message, "- Greetings message\n")
				if imp_gdbye:
					text += (update.effective_message, "- Goodbye message\n")
				if imp_locks:
					text += (update.effective_message, "- Locking\n")
				if imp_notes:
					text += (update.effective_message, "- {} Notes\n").format(imp_notes)
				if imp_rules:
					text += (update.effective_message, "- Group rules message\n")
				try:
					msg.reply_text(text, parse_mode="markdown")
				except BadRequest:
					msg.reply_text(text, parse_mode="markdown", quote=False)
				if NOT_IMPORTED_INT:
					f = open("{}-notimported.txt".format(chat_id), "w")
					f.write(str(NOT_IMPORTED))
					f.close()
					bot.sendDocument(chat_id, document=open('{}-notimported.txt'.format(chat_id), 'rb'), caption=tl(update.effective_message, "*Data that can't be imported*"), timeout=360, parse_mode=ParseMode.MARKDOWN)
					os.remove("{}-notimported.txt".format(chat_id))
				return
		except Exception as err:
			msg.reply_text(update.effective_message, "An error has occurred getting CTRL backup!\nGo, ping [my owner](https://t.me/refundisillegal) and ask if any solution of it!\n\nMaybe they can resolve your issue!", parse_mode="markdown")
			LOGGER.exception("An error when importing from CTRL base!")
			return

		try:
			# If backup is from rose
			# doing manual lol
			if data.get('bot_id') == 7815183153:
				imp_filters_count = 0
				imp_greet = False
				imp_gdbye = False
				imp_greet_pref = False
				imp_notes = 0
				imp_rules = False
				NOT_IMPORTED = "This cannot be imported because from other bot."
				NOT_IMPORTED_INT = 0
				if data.get('data'):
					# Import filters
					if data['data'].get('filters'):
						NOT_IMPORTED += "\n\nFilters:\n"
						if data['data']['filters'].get('filters'):
							for x in data['data']['filters'].get('filters'):
								if x['type'] == 0:
									note_data, buttons = button_markdown_parser(x['text'].replace("\\", ""), entities=0)
									filtersql.add_filter(chat_id, x['name'], note_data, False, False, False, False, False, False, buttons)
									imp_filters_count += 1
								else:
									NOT_IMPORTED += "- {}\n".format(x['name'])
									NOT_IMPORTED_INT += 1
					# Import greetings
					if data['data'].get('greetings'):
						if data['data']['greetings'].get('welcome'):
							welctext = data['data']['greetings']['welcome'].get('text')
							if welctext:
								note_data, buttons = button_markdown_parser(welctext.replace("\\", ""), entities=0)
								welcsql.set_custom_welcome(chat_id, None, note_data, Types.TEXT, buttons)
								imp_greet = True
						if data['data']['greetings'].get('goodbye'):
							gdbytext = data['data']['greetings']['goodbye'].get('text')
							if welctext:
								note_data, buttons = button_markdown_parser(gdbytext.replace("\\", ""), entities=0)
								welcsql.set_custom_gdbye(chat_id, None, note_data, Types.TEXT, buttons)
								imp_gdbye = True
						# Welcome config
						if data['data']['greetings'].get('should_welcome'):
							welcsql.set_welc_preference(str(chat_id), True)
						else:
							welcsql.set_welc_preference(str(chat_id), False)
						# Goodbye config
						if data['data']['greetings'].get('should_goodbye'):
							welcsql.set_gdbye_preference(str(chat_id), True)
						else:
							welcsql.set_gdbye_preference(str(chat_id), False)
						# clean service
						if data['data']['greetings'].get('should_delete_service'):
							welcsql.set_clean_service(chat_id, True)
						else:
							welcsql.set_clean_service(chat_id, False)
						# custom mute btn
						if data['data']['greetings'].get('mute_text'):
							getcur, cur_value, cust_text = welcsql.welcome_security(chat_id)
							welcsql.set_welcome_security(chat_id, getcur, cur_value, data['data']['greetings'].get('mute_text'))
						imp_greet_pref = True
						# TODO parsing unix time and import that
					# TODO Locks
					# Import notes
					if data['data'].get('notes'):
						NOT_IMPORTED += "\n\nNotes:\n"
						allnotes = data['data']['notes']['notes']
						for x in allnotes:
							# If this text
							if x['type'] == 0:
								note_data, buttons = button_markdown_parser(x['text'].replace("\\", ""), entities=0)
								note_name = x['name']
								notesql.add_note_to_db(chat_id, note_name, note_data, Types.TEXT, buttons, None)
								imp_notes += 1
							else:
								NOT_IMPORTED += "- {}\n".format(x['name'])
								NOT_IMPORTED_INT += 1
					# Import rules
					if data['data'].get('rules'):
						contrules = data['data']['rules'].get('content')
						if contrules:
							rulessql.set_rules(chat_id, contrules.replace("\\", ""))
							imp_rules = True
					if conn:
						text = (update.effective_message, "Backup is fully restored in*{}*. Welcome backup! :3").format(chat_name)
					else:
						text = (update.effective_message, "Backup fully recovered! \n it's it easy for me?!").format(chat_name)
					text += (update.effective_message, "\n\nWhat I return:\n")
					if imp_filters_count:
						text += (update.effective_message, "- {} filters\n").format(imp_filters_count)
					if imp_greet_pref:
						text += (update.effective_message, "- Greeting setting.\n")
					if imp_greet:
						text += (update.effective_message, "- Greeting message\n")
					if imp_gdbye:
						text += (update.effective_message, "- Goodbye message\n")
					if imp_notes:
						text += (update.effective_message, "- {} Notes\n").format(imp_notes)
					if imp_rules:
						text += (update.effective_message, "- Chat rules.\n")
					try:
						msg.reply_text(text, parse_mode="markdown")
					except BadRequest:
						msg.reply_text(text, parse_mode="markdown", quote=False)
					if NOT_IMPORTED_INT:
						f = open("{}-notimported.txt".format(chat_id), "w")
						f.write(str(NOT_IMPORTED))
						f.close()
						bot.sendDocument(chat_id, document=open('{}-notimported.txt'.format(chat_id), 'rb'), caption=tl(update.effective_message, "*Data yang tidak dapat di import*"), timeout=360, parse_mode=ParseMode.MARKDOWN)
						os.remove("{}-notimported.txt".format(chat_id))
					return
		except Exception as err:
			msg.reply_text(update.effective_message, "An error occurred when importing Rose backup!\nGo, ping [my owner](https://t.me/Kingofelephants) and ask if any solution of it!\n\nMaybe they can resolve your goddamn issue!", parse_mode="markdown")
			LOGGER.exception("An error when importing from Rose base!")
			return

		# only import one group
		if len(data) > 1 and str(chat_id) not in data:
			msg.reply_text(tl(update.effective_message, "There are more than one chat in this fukin file."
						   "and no-one has the same ID as this chat- how do I choose what to import?"))
			return

		# Check if backup is this chat
		try:
			if data.get(str(chat_id)) == None:
				if conn:
					text = (update.effective_message, "Backup originates from another chat, I can't return another chat to this chat *{}*").format(chat_name)
				else:
					text = (update.effective_message, "F, Backup originates are from another chat, I can't return another chat to this chat!")
				return msg.reply_text(text, parse_mode="markdown")
		except:
			return msg.reply_text(tl(update.effective_message, "An error has occurred in checking the data, please report it to my author"
"for this problem to make me better! Thank you!"))
		# Check if backup is from self
		try:
			if str(bot.id) != str(data[str(chat_id)]['bot']):
				return msg.reply_text(tl(update.effective_message, "Backups come from other bots, documents, photos, videos, audio, sound will not"
"works, if your files don't want to be lost, import from a backed up bot."
"if it still doesn't work, report it to the owner (@KingOfElephants) to"
"makes me better! Thanks!"))
		except:
			pass
		# Select data source
		if str(chat_id) in data:
			data = data[str(chat_id)]['hashes']
		else:
			data = data[list(data.keys())[0]]['hashes']

		try:
			for mod in DATA_IMPORT:
				mod.__import_data__(str(chat_id), data)
		except Exception:
			msg.reply_text(tl(update.effective_message, "An error occurred while restoring your data. The process might not be complete. If"
"You are having problems with this, the message @KingOfElephants with your backup file, so"
"the problem can be debugged. My owner will be happy to help, and any bugs"
"reportedly makes me better! Thank you!"))
			LOGGER.exception("Import from chat ID %s with chat name %s failed.", str(chat_id), str(chat.title))
			return

		# TODO: some of that link logic
		# NOTE: consider default permissions stuff?
		if conn:
			text = (update.effective_message, "Backup is funny restored in *{}*. Welcome back!").format(chat_name)
		else:
			text = (update.effective_message, "Backup has fully recovered. \n welcome back! ").format(chat_name)
		msg.reply_text(text, parse_mode="markdown")


@run_async
@user_admin
def export_data(bot: Bot, update: Update, chat_data):
	msg = update.effective_message  # type: Optional[Message]
	user = update.effective_user  # type: Optional[User]
	chat_id = update.effective_chat.id
	chat = update.effective_chat
	current_chat_id = update.effective_chat.id

	conn = connected(bot, update, chat, user.id, need_admin=True)
	if conn:
		chat = dispatcher.bot.getChat(conn)
		chat_id = conn
		chat_name = dispatcher.bot.getChat(conn).title
	else:
		if update.effective_message.chat.type == "private":
			update.effective_message.reply_text(update.effective_message, "Anda bisa lakukan command ini pada grup, bukan pada PM")
			return ""
		chat = update.effective_chat
		chat_id = update.effective_chat.id
		chat_name = update.effective_message.chat.title

	jam = time.time()
	new_jam = jam + 43200
	cek = get_chat(chat_id, chat_data)
	if cek.get('status'):
		if jam <= int(cek.get('value')):
			waktu = time.strftime("%H:%M:%S %d/%m/%Y", time.localtime(cek.get('value')))
			update.effective_message.reply_text(update.effective_message, "Anda dapat mencadangan data sekali dalam 12 jam!\n[Orang ini](tg://user?id={}) sudah mencadangan data\nAnda dapat mencadangan data lagi pada `{}`".format(cek.get('user'), waktu), parse_mode=ParseMode.MARKDOWN)
			return
		else:
			if user.id != OWNER_ID:
				put_chat(chat_id, user.id, new_jam, chat_data)
	else:
		if user.id != OWNER_ID:
			put_chat(chat_id, user.id, new_jam, chat_data)


	# Backup version
	# Revision: 07/07/2019
	backup_ver = 1
	bot_base = "Julie"

	# Make sure this backup is for this bot
	bot_id = bot.id

	# Backuping filters
	all_filters = filtersql.get_chat_triggers(chat_id)
	filters_gen = []
	for x in all_filters:
		filt = filtersql.get_filter(chat.id, x)
		if filt.is_sticker:
			filt_type = 1
		elif filt.is_document:
			filt_type = 2
		elif filt.is_image:
			filt_type = 3
		elif filt.is_audio:
			filt_type = 4
		elif filt.is_voice:
			filt_type = 5
		elif filt.is_video:
			filt_type = 6
		elif filt.has_markdown:
			filt_type = 0
		else:
			filt_type = 7
		filters_gen.append({"name": x, "reply": filt.reply, "type": filt_type})
	filters = {'filters': filters_gen}

	# Backuping greetings msg and config
	greetings = {}
	pref, welcome_m, cust_content, welcome_type = welcsql.get_welc_pref(chat_id)
	if not welcome_m:
		welcome_m = ""
	if not cust_content:
		cust_content = ""
	buttons = welcsql.get_welc_buttons(chat_id)
	welcome_m += revert_buttons(buttons)
	greetings["welcome"] = {"enable": pref, "text": welcome_m, "content": cust_content, "type": welcome_type}

	pref, goodbye_m, cust_content, goodbye_type = welcsql.get_gdbye_pref(chat_id)
	if not goodbye_m:
		goodbye_m = ""
	if not cust_content:
		cust_content = ""
	buttons = welcsql.get_gdbye_buttons(chat_id)
	goodbye_m += revert_buttons(buttons)
	greetings["goodbye"] = {"enable": pref, "text": goodbye_m, "content": cust_content, "type": goodbye_type}

	curr = welcsql.clean_service(chat_id)
	greetings["clean_service"] = curr

	getcur, cur_value, cust_text = welcsql.welcome_security(chat_id)
	greetings["security"] = {"enable": getcur, "text": cust_text, "time": cur_value}

	# Backuping locks
	curr_locks = locksql.get_locks(chat_id)
	curr_restr = locksql.get_restr(chat_id)

	if curr_locks:
		locked_lock = {
			"sticker": curr_locks.sticker,
			"audio": curr_locks.audio,
			"voice": curr_locks.voice,
			"document": curr_locks.document,
			"video": curr_locks.video,
			"contact": curr_locks.contact,
			"photo": curr_locks.photo,
			"gif": curr_locks.gif,
			"url": curr_locks.url,
			"bots": curr_locks.bots,
			"forward": curr_locks.forward,
			"game": curr_locks.game,
			"location": curr_locks.location,
			"rtl": curr_locks.rtl
		}
	else:
		locked_lock = {}

	if curr_restr:
		locked_restr = {
			"messages": curr_restr.messages,
			"media": curr_restr.media,
			"other": curr_restr.other,
			"previews": curr_restr.preview,
			"all": all([curr_restr.messages, curr_restr.media, curr_restr.other, curr_restr.preview])
		}
	else:
		locked_restr = {}

	lock_warn = locksql.get_lockconf(chat_id)

	locks = {'lock_warn': lock_warn, 'locks': locked_lock, 'restrict': locked_restr}

	# Backuping notes
	note_list = notesql.get_all_chat_notes(chat_id)
	notes = []
	for note in note_list:
		buttonlist = ""
		note_tag = note.name
		note_type = note.msgtype
		getnote = notesql.get_note(chat_id, note.name)
		if not note.value:
			note_data = ""
		else:
			tombol = notesql.get_buttons(chat_id, note_tag)
			keyb = []
			buttonlist = ""
			for btn in tombol:
				if btn.same_line:
					buttonlist += "[{}](buttonurl:{}:same)\n".format(btn.name, btn.url)
				else:
					buttonlist += "[{}](buttonurl:{})\n".format(btn.name, btn.url)
			note_data = "{}\n\n{}".format(note.value, buttonlist)
		note_file = note.file
		if not note_file:
			note_file = ""
		notes.append({"note_tag": note_tag, "note_data": note_data, "note_file": note_file, "note_type": note_type})

	# Backuping rules
	getrules = rulessql.get_rules(chat_id)
	rules = {"rules": getrules}


	# Parsing backups
	backup = {"bot_id": bot_id, "bot_base": bot_base, "filters": filters, "greetings": greetings,  "locks": locks, "notes": notes, "rules": rules, "version": backup_ver}


	all_backups = json.dumps(backup, indent=4, cls=SetEncoder)
	f = open("{}-Monica.backup".format(chat_id), "w")
	f.write(str(all_backups))
	f.close()
	bot.sendChatAction(current_chat_id, "upload_document")
	tgl = time.strftime("%H:%M:%S - %d/%m/%Y", time.localtime(time.time()))
	try:
		bot.sendMessage(TEMPORARY_DATA, "*Successfully backed up for:*\nNama chat: `{}`\nID chat: `{}`\non: `{}`".format(chat.title, chat_id, tgl), parse_mode=ParseMode.MARKDOWN)
	except BadRequest:
		pass
	send = bot.sendDocument(current_chat_id, document=open('{}-Julie.backup'.format(chat_id), 'rb'), caption=(update.effective_message, "*Successfully backed up for:*\nChat Name: `{}`\nID chat: `{}`\non: `{}`\n\nNote: cadangan ini khusus untuk bot ini, jika di import ke bot lain maka catatan dokumen, video, audio, voice, dan lain-lain akan hilang").format(chat.title, chat_id, tgl), timeout=360, reply_to_message_id=msg.message_id, parse_mode=ParseMode.MARKDOWN)
	try:
		# Send to temp data for prevent unexpected issue
		bot.sendDocument(TEMPORARY_DATA, document=send.document.file_id, caption=(update.effective_message, "*Successfully backed up for:*\nChat Name: `{}`\nID chat: `{}`\non: `{}`\n\nNote: cadangan ini khusus untuk bot ini, jika di import ke bot lain maka catatan dokumen, video, audio, voice, dan lain-lain akan hilang").format(chat.title, chat_id, tgl), timeout=360, parse_mode=ParseMode.MARKDOWN)
	except BadRequest:
		pass
	os.remove("{}-Julie.backup".format(chat_id)) # Cleaning file


class SetEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, set):
			return list(obj)
		return json.JSONEncoder.default(self, obj)


# Temporary data
def put_chat(chat_id, user_id, value, chat_data):
	# print(chat_data)
	if value == False:
		status = False
	else:
		status = True
	chat_data[chat_id] = {'backups': {"status": status, "user": user_id, "value": value}}

def get_chat(chat_id, chat_data):
	# print(chat_data)
	try:
		value = chat_data[chat_id]['backups']
		return value
	except KeyError:
		return {"status": False, "user": None, "value": False}


__mod_name__ = "Import/Export"

__help__ = "backups_help"

IMPORT_HANDLER = CommandHandler("import", import_data, filters=Filters.group)
EXPORT_HANDLER = CommandHandler("export", export_data, pass_chat_data=True)
# EXPORT_HANDLER = CommandHandler("export", export_data, filters=Filters.user(OWNER_ID))

dispatcher.add_handler(IMPORT_HANDLER)
dispatcher.add_handler(EXPORT_HANDLER)
