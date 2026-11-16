"""Episode content. Each segment = one shell-opening with three items.
Lines are lists of (lang, text) parts; the LAST "en" part of an aligned line is the English key word:
both tracks are shifted so the key word is spoken at the same moment, when it appears on screen."""

SEGMENTS = {
    "colors": dict(
        word_color=["#E94B3C", "#FFC93C", "#3C8DE9"],
        items=[
            dict(kind="ball_red", name="red ball", tr_name="Kırmızı top", word="RED",
                 en=[("en", "Wow! A ball!"), ("en", "Red!")], tr=[("tr", "Vay! Kırmızı bir top!"), ("en", "Red!")]),
            dict(kind="ball_yellow", name="yellow ball", tr_name="Sarı top", word="YELLOW",
                 en=[("en", "Another one!"), ("en", "Yellow!")], tr=[("tr", "Bir tane daha! Sarı!"), ("en", "Yellow!")]),
            dict(kind="ball_blue", name="blue ball", tr_name="Mavi top", word="BLUE",
                 en=[("en", "And..."), ("en", "Blue!")], tr=[("tr", "Ve... mavi!"), ("en", "Blue!")]),
        ],
        summary=dict(word="3 balls!", en=[("en", "Three bouncy balls!")], tr=[("tr", "Üç top!"), ("en", "Three balls!")]),
    ),
    "animals": dict(
        word_color=["#E07A2E", "#8B5E3C", "#E0A800"],
        items=[
            dict(kind="cat", name="cat", tr_name="Kedi", word="CAT",
                 en=[("en", "Look! Meow, meow!"), ("en", "A cat!")], tr=[("tr", "Bak! Miyav, miyav! Bir kedi!"), ("en", "Cat!")]),
            dict(kind="dog", name="dog", tr_name="Köpek", word="DOG",
                 en=[("en", "Woof, woof!"), ("en", "A dog!")], tr=[("tr", "Hav, hav! Bir köpek!"), ("en", "Dog!")]),
            dict(kind="duck", name="duck", tr_name="Ördek", word="DUCK",
                 en=[("en", "Quack, quack!"), ("en", "A duck!")], tr=[("tr", "Vak, vak! Bir ördek!"), ("en", "Duck!")]),
        ],
        summary=dict(word="3 animals!", en=[("en", "Three animal friends!")], tr=[("tr", "Üç hayvan!"), ("en", "Three animals!")]),
    ),
    "shapes": dict(
        word_color=["#2FA36B", "#7B4BC8", "#E86A1C"],
        items=[
            dict(kind="circle", name="circle", tr_name="Daire", word="CIRCLE",
                 en=[("en", "Look! It's round!"), ("en", "Circle!")], tr=[("tr", "Bak! Yuvarlak bir daire!"), ("en", "Circle!")]),
            dict(kind="square", name="square", tr_name="Kare", word="SQUARE",
                 en=[("en", "Four sides!"), ("en", "Square!")], tr=[("tr", "Dört kenarlı bir kare!"), ("en", "Square!")]),
            dict(kind="triangle", name="triangle", tr_name="Üçgen", word="TRIANGLE",
                 en=[("en", "Three points!"), ("en", "Triangle!")], tr=[("tr", "Üç köşeli bir üçgen!"), ("en", "Triangle!")]),
        ],
        summary=dict(word="3 shapes!", en=[("en", "Three shapes!")], tr=[("tr", "Üç şekil!"), ("en", "Three shapes!")]),
    ),
}

SEGMENTS["fruits"] = dict(
    word_color=["#E63946", "#E0A800", "#F07B00"],
    items=[
        dict(kind="apple", name="apple", tr_name="Elma", word="APPLE",
             en=[("en", "Yummy! Crunch, crunch!"), ("en", "Apple!")], tr=[("tr", "Kıtır kıtır! Bir elma!"), ("en", "Apple!")]),
        dict(kind="banana", name="banana", tr_name="Muz", word="BANANA",
             en=[("en", "Long and yellow!"), ("en", "Banana!")], tr=[("tr", "Uzun ve sarı bir muz!"), ("en", "Banana!")]),
        dict(kind="orange", name="orange", tr_name="Portakal", word="ORANGE",
             en=[("en", "Round and juicy!"), ("en", "Orange!")], tr=[("tr", "Yuvarlak, sulu bir portakal!"), ("en", "Orange!")]),
    ],
    summary=dict(word="3 fruits!", en=[("en", "Three yummy fruits!")], tr=[("tr", "Üç meyve!"), ("en", "Three fruits!")]),
)

INTRO = dict(en=[("en", "Hi friends! I'm Tosbi!")], tr=[("tr", "Merhaba arkadaşlar! Ben Tosbi!")])
ASK = dict(en=[("en", "What's inside my shell today?")], tr=[("tr", "Bugün kabuğumda ne var acaba?")])
ASK_AGAIN = dict(en=[("en", "Let's see what else is inside!")], tr=[("tr", "Hadi bakalım, kabuğumda başka ne var?")])
KNOCK = dict(en=[("en", "Let's knock!"), ("en", "Knock, knock!")], tr=[("tr", "Hadi tıklatalım!"), ("en", "Knock, knock!")])
REPEAT = dict(en=[("en", "Say it with me!")], tr=[("tr", "Hadi sen de söyle!")])
COUNT = dict(en=[("en", "Let's count them!")], tr=[("tr", "Hadi İngilizce sayalım!")])
NUMS = [[("en", "One!")], [("en", "Two!")], [("en", "Three!")]]
OUTRO = dict(en=[("en", "What will be in my shell tomorrow?"), ("en", "Bye-bye!")],
             tr=[("tr", "Yarın kabuğumda ne olacak? Hoşça kalın!"), ("en", "Bye-bye!")])

QUIZ_INTRO = dict(en=[("en", "Let's play a game!")], tr=[("tr", "Hadi bir oyun oynayalım!")])
def quiz_q(it):
    return [("en", f"Where is the {it['name']}?")], [("tr", f"{it['tr_name']} nerede?")]
def quiz_a(it):
    w = [("en", it["word"].capitalize() + "!")]
    return [("en", "There it is!")] + w, [("tr", "İşte orada!")] + w

# ---- week 2026-11-16
# Parts may carry a third element "zip" = spoken by Zıpzıp (own voice + mouth). Default speaker = Tosbi.
SEGMENTS["farm"] = dict(
    word_color=["#8B5E3C", "#7B4BC8", "#E94B3C"],
    items=[
        dict(kind="cow", name="cow", tr_name="İnek", word="COW",
             en=[("en", "Moo, moo!"), ("en", "A cow!")], tr=[("tr", "Mö, mö! Bir inek!"), ("en", "Cow!")]),
        dict(kind="sheep", name="sheep", tr_name="Koyun", word="SHEEP",
             en=[("en", "Baa, baa!"), ("en", "A sheep!")], tr=[("tr", "Me, me! Bir koyun!"), ("en", "Sheep!")]),
        dict(kind="chicken", name="chicken", tr_name="Tavuk", word="CHICKEN",
             en=[("en", "Cluck, cluck!"), ("en", "A chicken!")], tr=[("tr", "Gıt gıt gıdak! Bir tavuk!"), ("en", "Chicken!")]),
    ],
    summary=dict(word="Farm friends!", en=[("en", "Three farm friends!")], tr=[("tr", "Üç çiftlik hayvanı!"), ("en", "Farm friends!")]),
)

SEGMENTS["things"] = dict(
    word_color=["#3C8DE9", "#E94B3C", "#7B4BC8"],
    items=[
        dict(kind="cup", name="cup", tr_name="Bardak", word="CUP",
             en=[("en", "Sip, sip!"), ("en", "A cup!")], tr=[("tr", "Höp höp! Bir bardak!"), ("en", "Cup!")]),
        dict(kind="hat", name="hat", tr_name="Şapka", word="HAT",
             en=[("en", "On my head!"), ("en", "A hat!")], tr=[("tr", "Başıma takarım! Bir şapka!"), ("en", "Hat!")]),
        dict(kind="shoe", name="shoe", tr_name="Ayakkabı", word="SHOE",
             en=[("en", "On my foot!"), ("en", "A shoe!")], tr=[("tr", "Ayağıma giyerim! Bir ayakkabı!"), ("en", "Shoe!")]),
    ],
    summary=dict(word="3 things!", en=[("en", "Three things for me!")], tr=[("tr", "Üç eşya!"), ("en", "Three things!")]),
)

# First episode with Zıpzıp (theme: taking turns). friend=True -> Zıpzıp hops in after the question.
SEGMENTS["vehicles"] = dict(
    friend=True,
    word_color=["#E94B3C", "#E0A800", "#3C8DE9"],
    items=[
        dict(kind="car", name="car", tr_name="Araba", word="CAR",
             en=[("en", "Beep, beep!"), ("en", "A car!")], tr=[("tr", "Bip, bip! Bir araba!"), ("en", "Car!")]),
        dict(kind="bus", name="bus", tr_name="Otobüs", word="BUS",
             en=[("en", "My turn! Honk, honk!", "zip"), ("en", "A bus!", "zip")],
             tr=[("tr", "Sıra bende! Düt düt! Bir otobüs!", "zip"), ("en", "Bus!", "zip")]),
        dict(kind="boat", name="boat", tr_name="Tekne", word="BOAT",
             en=[("en", "Your turn, Tosbi!", "zip"), ("en", "Splash, splash!"), ("en", "A boat!")],
             tr=[("tr", "Sıra sende Tosbi!", "zip"), ("tr", "Şıpır şıpır! Bir tekne!"), ("en", "Boat!")]),
    ],
    summary=dict(word="3 vehicles!", en=[("en", "Three vehicles!")], tr=[("tr", "Üç taşıt!"), ("en", "Three vehicles!")]),
)

FRIEND_HELLO = dict(en=[("en", "Hi Tosbi! I'm Zipzip!", "zip"), ("en", "Me first! Me first!", "zip")],
                    tr=[("tr", "Merhaba Tosbi! Ben Zıpzıp! Önce ben, önce ben!", "zip")])
TAKE_TURNS = dict(en=[("en", "Hi Zipzip!"), ("en", "Let's take turns!")],
                  tr=[("tr", "Merhaba Zıpzıp! Hadi sırayla yapalım."), ("en", "Take turns!")], word="Take turns!")
FRIEND_BYE = dict(en=[("en", "Taking turns is fun!", "zip")], tr=[("tr", "Sırayla oynamak çok eğlenceli!", "zip")])
