import html

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest

from jmub.Config import Config
from jmub.plugins import (
    ALIVE_NAME,
    BOTLOG,
    BOTLOG_CHATID,
    edit_delete,
    get_user_from_event,
    jmub,
)
from jmub.sql_helper.globals import gvarstatus

DEFAULTUSER = gvarstatus("FIRST_NAME") or ALIVE_NAME
DEFAULTUSERBIO = Config.DEFAULT_BIO or "﴿ لا تَحزَن إِنَّ اللَّهَ مَعَنا ﴾"
ANT7AL = gvarstatus("ANT7AL") or "(اعادة الحساب|اعادة)"


@jmub.ar_cmd(pattern="انتحال(?:\s|$)([\s\S]*)")
async def _(event):
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user.id == 5092041118:
        return await edit_delete(event, "**بسعيب يولاه دي المطورة**")
    if replied_user.id == 5190136458:
        return await edit_delete(event, "**بسعيب يولاه ده المطور**")
    if replied_user.id == 1001132193:
        return await edit_delete(event, "**بسعيب يولاه ده المطور**")
    if replied_user.id == 627658332:
        return await edit_delete(event, "**بسعيب يولاه ده المطور**")
    if replied_user.id == 1833610203:
        return await edit_delete(event, "**بسعيب يولاه ده المطور**")    
    if replied_user is None:
         return
    user_id = replied_user.id
    profile_pic = await event.client.download_profile_photo(user_id, Config.TEMP_DIR)
    first_name = html.escape(replied_user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    replied_user = (await event.client(GetFullUserRequest(replied_user.id))).full_user
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await event.client(functions.account.UpdateProfileRequest(first_name=first_name))
    await event.client(functions.account.UpdateProfileRequest(last_name=last_name))
    await event.client(functions.account.UpdateProfileRequest(about=user_bio))
    try:
        pfile = await event.client.upload_file(profile_pic)
    except Exception as e:
        return await edit_delete(event, f"**فشل في الانتحال بسبب:**\n__{e}__")
    await event.client(functions.photos.UploadProfilePhotoRequest(pfile))
    await edit_delete(event, "**⌁︙تـم نسـخ الـحساب بـنجاح ،✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#الانتحال\nتم انتحال المستخدم: [{first_name}](tg://user?id={user_id })",
        )


@jmub.ar_cmd(
    pattern="اعادة$",
    command=("اعادة", plugin_category),
    info={
        "header": "To revert back to your original name , bio and profile pic",
        "note": "For proper Functioning of this command you need to set AUTONAME and DEFAULT_BIO with your profile name and bio respectively.",
        "usage": "{tr}revert",
    },
)
async def _(event):
    "To reset your original details"
    name = f"{DEFAULTUSER}"
    blank = ""
    bio = f"{DEFAULTUSERBIO}"
    await event.client(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=1)
        )
    )
    await event.client(functions.account.UpdateProfileRequest(about=bio))
    await event.client(functions.account.UpdateProfileRequest(first_name=name))
    await event.client(functions.account.UpdateProfileRequest(last_name=blank))
    await edit_delete(event, "⌁︙تـم اعـادة الـحساب بـنجاح ،✅")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"⌁︙تـم اعادة الـحساب الى وضـعه الاصلـي ،✅")
        
