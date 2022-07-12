from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import textwrap


def visitmake(userid, username, name, surname, city, role, superpower, year):
    im2 = Image.open('photo_user/'+userid+'.jpg')
    im1 = Image.open('img/visit.png')
    superpower = textwrap.fill(text=superpower, width=35)
    im2 = im2.convert("L")
    mask_im = Image.new("1", im2.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((142, 109, 957, 916), fill=255)
    im1.paste(im2, (315, 0), mask_im)
    font = ImageFont.truetype('fonds/Gilroy-Medium.ttf', size=36)
    font1 = ImageFont.truetype('fonds/Gilroy-Medium.ttf', size=30)
    font2 = ImageFont.truetype('fonds/Gilroy-Medium.ttf', size=25)
    font3 = ImageFont.truetype('fonds/Gilroy-Medium.ttf', size=24)
    draw_text = ImageDraw.Draw(im1)
    draw_text.text(
        (140, 85),
        '@'+username,
        font=font,
        fill='#ffffff')
    draw_text.text(
        (80, 240),
        name,
        font=font1,
        fill='#ffffff')
    draw_text.text(
        (80, 275),
        surname,
        font=font1,
        fill='#ffffff')
    draw_text.text(
        (80, 455),
        city,
        font=font2,
        fill='#ffffff')
    draw_text.text(
        (80, 625),
        role,
        font=font2,
        fill='#ffffff')
    draw_text.text(
        (80, 808),
        superpower,
        font=font2,
        fill='#ffffff')
    draw_text.text(
        (450, 1105),
        year,
        font=font3,
        fill='#000000')
    im1.save('visits/'+str(userid)+'_visit'+'.png', quality=95)
    im1.close()
    im2.close()
    mask_im.close()
    return userid

