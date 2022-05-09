import os
import logging
import bot.constants as con
from typing import Dict

from telegram import (
    Update,
    ParseMode,
    BotCommand,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def facts_to_str(user_data: Dict[str, str]):
    nombre = user_data['nombre']
    episodios = user_data['episodios']
    temporada = user_data['temporada']
    tipo = user_data['tipo']
    ano = user_data['ano']
    audio = user_data['audio']
    subtitulos = user_data['subtitulos']
    resolucion = user_data['resolucion']
    genero = user_data['genero']
    sinopsis = user_data['sinopsis']
    return (
        f'🎐<b>{nombre}</b>🎐\n\n\n🎞 <b>Episodios:</b> {episodios}\n\n🎬 <b>Temporada:</b> {temporada}\n\n📺 <b>Tipo:</b> {tipo}\n\n📅 <b>Año:</b> {ano}\n\n🎧 <b>Audio:</b> {audio}\n\n'
        f'📝 <b>Subtítulos:</b> {subtitulos}\n\n📽 <b>Resolución:</b> {resolucion}\n\n🎭 <b>Género:</b> {genero}\n\n'
        f'📃  <b>Sinopsis:</b> {sinopsis}\n\n'
        '⛩🎐🎐🎐🎐🎐🎐🎐🎐🎐🎐🎐🎐🎐🎐🎐⛩\n🎐 <a href="https://t.me/+xIxuRUxYjs4zNDJh"><b>X Anime Finalizados</b></a> 🎐'
    )


def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    if user_id in con.administradores:
        update.message.reply_text(
            text=f'Hola <a href="tg://user?id={user_id}">{first_name}</a>\nPulsa /comenzar para generar una plantilla.',
            parse_mode=ParseMode.HTML
            )
        context.bot.set_my_commands([
            BotCommand(command='comenzar', description='Generar una plantilla.'),
            BotCommand(command='cancelar', description='Detener el proceso actual.')
            ]
        )
    else:
        update.message.reply_text(
            text=f'<a href="tg://user?id={user_id}">{first_name}</a> no tienes acceso para usar este bot.',
            parse_mode=ParseMode.HTML
            )


def comenzar(update: Update, context: CallbackContext):
    if update.effective_user.id in con.administradores:
        update.message.reply_text(
            "Enviame la imagen de la Serien Pelicula.",
            )
        return con.PHOTO


def photo(update: Update, context: CallbackContext):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('bot/photo/{}.jpg'.format(update.message.chat_id))
    update.message.reply_text(
        'Enviame el nombre de la Serie o Película.'
    )
    return con.NOMBRE


def nombre(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['nombre'] = text
    update.message.reply_text(
        f'Dime los episodios si es pelicula no espesificar ---.'
    )
    return con.EPISODIOS



def episodios(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['episodios'] = text
    update.message.reply_text(
        f'Enviame la Temporadas si es pelicula dejar ---.'
    )
    return con.TEMPORADA


def temporada(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['temporada'] = text
    update.message.reply_text(
        f'Envia el tipo que es: \n#Serie #Pelicula #OVA #Special '
    )
    return con.TIPO


def tipo(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['tipo'] = text
    update.message.reply_text(
        f'Enviame el año en que fue lanzada la serie.'
    )
    return con.ANO


def ano(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['ano'] = text
    update.message.reply_text(
        f'Enviame en que idioma esta el audio: \n#Español #Ingles #Japones \n#Dual_Audio.'
    )
    return con.AUDIO


def audio(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['audio'] = text
    update.message.reply_text(
        f'En que idioma están los subtitulos: \n#Español #Ingles #Multisubtitulos.'
    )
    return con.SUBTITULOS


def subtitulos(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['subtitulos'] = text
    update.message.reply_text(
        f'Digame el genero: \n#Accion \n#Artes_Marciales #Aventuras \n#Carreras #Ciencia_Ficcion \n#Comedia #Demonios \n#Deportes #Drama \n#Ecchi #Escolares \n#Espacial #Fantasia \n#Harem #Infantil \n#Josei #Juegos \n#Magia #Mecha \n#Militar #Misterio \n#Musica #Parodia \n#Policia #Psicologico \n#Recuerdos_de_la_vida #Romance \n#Samurai #Seinen \n#Shoujo #Shounen \n#Superpoderes #Suspenso \n#Terror #Vampiros \n#Yaoi #Yuri #Hentai '
    )
    return con.GENERO


def genero(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['genero'] = text
    update.message.reply_text(
        f'mmm.'
    )
    return con.SINOPSIS


def sinopsis(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['sinopsis'] = text

    update.message.reply_text(
        text=f"✅ Plantilla creada correctamente\n<b>Resultado:</b>\n\n{facts_to_str(context.user_data)}".format(user=user_id, name=first_name) +
            "\n\nPulsa el botón de debajo para enviar la plantilla. 📢",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup([['Enviar plantilla ✅']],
            one_time_keyboard=True,
            resize_keyboard=True
            )
        )
    return con.SEND


def done(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name


    context.bot.send_photo(
        chat_id=con.CHANNEL,
        photo=open(f'bot/photo/{update.message.chat_id}.jpg', 'rb'),
        caption=f'{facts_to_str(user_data)}'.format(user=user_id, name=first_name),
        parse_mode=ParseMode.HTML,
    )
    user_data.clear()
    return ConversationHandler.END


def stop(update: Update, context: CallbackContext):
    if update.effective_user.id in con.administradores:
        update.message.reply_text(
            text='Operación cancelada.',
            reply_markup=ReplyKeyboardRemove(selective=True)
        )
        return ConversationHandler.END

def main():
    token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('comenzar', comenzar)],
        states={
            con.PHOTO: [
                MessageHandler(Filters.photo, photo),
            ],
            con.NOMBRE: [
                MessageHandler(Filters.text, nombre)
            ],
            con.LINK: [
                MessageHandler(Filters.text, link)
            ],
            con.DESCRIPCION: [
                MessageHandler(Filters.text, descripcion)
            ],
            con.CONTENIDO_SUBIR: [
                MessageHandler(Filters.text, contenido)
            ],
            con.PALABRA_CREADOR: [
                MessageHandler(Filters.text, palabras)
            ],
            con.VALORACION: [
                MessageHandler(Filters.text, valoracion),
            ],
            con.SEND: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Enviar plantilla ✅$')), done),
            ],
        },
        fallbacks=[
            MessageHandler(Filters.regex('^Enviar plantilla ✅$'), done),
            CommandHandler('cancelar', stop),
            ],
        allow_reentry=True
    )
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()