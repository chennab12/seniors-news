"""Content for the helper pages (scam checker, emergency card, hospitals, dates, check-ups), in English and Telugu."""
from urllib.parse import quote

HYDERABAD = (17.385, 78.4867)


def maps_link(query):
    return "https://www.google.com/maps/search/?api=1&query=" + quote(query)


# Government hospitals: (icon, name, Telugu name, what for, Telugu what for, map search)
HOSPITALS = [
    ("🏥", "NIMS, Punjagutta", "నిమ్స్, పంజాగుట్ట", "Government super-speciality hospital", "ప్రభుత్వ సూపర్ స్పెషాలిటీ ఆసుపత్రి", "NIMS Hospital Punjagutta Hyderabad"),
    ("🏥", "Gandhi Hospital, Musheerabad", "గాంధీ ఆసుపత్రి, ముషీరాబాద్", "Large government general hospital", "పెద్ద ప్రభుత్వ సాధారణ ఆసుపత్రి", "Gandhi Hospital Hyderabad"),
    ("🏥", "Osmania General Hospital, Afzalgunj", "ఉస్మానియా జనరల్ ఆసుపత్రి, అఫ్జల్‌గంజ్", "Large government general hospital", "పెద్ద ప్రభుత్వ సాధారణ ఆసుపత్రి", "Osmania General Hospital Hyderabad"),
    ("👁️", "Sarojini Devi Eye Hospital, Mehdipatnam", "సరోజినీ దేవి కంటి ఆసుపత్రి, మెహదీపట్నం", "Government eye hospital (cataract, glaucoma)", "ప్రభుత్వ కంటి ఆసుపత్రి (కంటిశుక్లం, గ్లాకోమా)", "Sarojini Devi Eye Hospital Hyderabad"),
    ("👂", "Government ENT Hospital, Koti", "ప్రభుత్వ ENT ఆసుపత్రి, కోఠి", "Ear, nose and throat", "చెవి, ముక్కు, గొంతు", "Government ENT Hospital Koti Hyderabad"),
    ("🎗️", "MNJ Cancer Hospital, Red Hills", "MNJ క్యాన్సర్ ఆసుపత్రి, రెడ్ హిల్స్", "Government cancer hospital", "ప్రభుత్వ క్యాన్సర్ ఆసుపత్రి", "MNJ Cancer Hospital Hyderabad"),
    ("🏥", "King Koti District Hospital", "కింగ్ కోఠి జిల్లా ఆసుపత్రి", "Government district hospital", "ప్రభుత్వ జిల్లా ఆసుపత్రి", "King Koti District Hospital Hyderabad"),
]

NEAR_ME = [
    ("🏥", "Nearest hospital", "దగ్గరి ఆసుపత్రి", "hospital near me"),
    ("💊", "Jan Aushadhi store", "జన ఔషధి షాపు", "Jan Aushadhi Kendra near me"),
    ("🌙", "24-hour pharmacy", "24 గంటల మందుల షాపు", "24 hour pharmacy near me"),
]

JAN_AUSHADHI = {
    "en": [
        "💊 Jan Aushadhi Kendras sell quality generic medicines that usually cost 50% to 90% less than branded ones.",
        "📝 Ask your doctor to write the medicine's generic (salt) name, so you can buy it at a Jan Aushadhi store.",
        "📱 The 'Jan Aushadhi Sugam' app shows nearby stores and medicine prices.",
        "⚠️ Do not switch a medicine on your own. Show the generic option to your doctor or pharmacist first.",
    ],
    "te": [
        "💊 జన ఔషధి కేంద్రాలు నాణ్యమైన జెనరిక్ మందులను అమ్ముతాయి. ఇవి సాధారణంగా బ్రాండెడ్ మందుల కంటే 50% నుండి 90% తక్కువ ధరకు ఉంటాయి.",
        "📝 జన ఔషధి షాపులో కొనడానికి వీలుగా, మందు యొక్క జెనరిక్ (సాల్ట్) పేరు రాయమని డాక్టర్‌ను అడగండి.",
        "📱 'జన ఔషధి సుగమ్' యాప్‌లో దగ్గరి షాపులు, మందుల ధరలు చూడవచ్చు.",
        "⚠️ మీ అంతట మీరే మందు మార్చకండి. ముందుగా జెనరిక్ మందును డాక్టర్ లేదా ఫార్మసిస్ట్‌కు చూపించండి.",
    ],
}

# Yearly reminders: (month, day, icon, English, Telugu)
IMPORTANT_DATES = [
    (3, 1, "☀️", "Summer is coming: check fans and coolers, keep ORS packets at home", "వేసవి వస్తోంది: ఫ్యాన్లు, కూలర్లు సరిచూసుకోండి, ఇంట్లో ORS ప్యాకెట్లు ఉంచండి"),
    (4, 1, "📝", "Give Form 15H to your bank so tax is not cut from FD interest", "FD వడ్డీపై పన్ను కోత లేకుండా బ్యాంకుకు ఫారం 15H ఇవ్వండి"),
    (4, 15, "🏠", "GHMC property tax early-bird rebate: check this year's last date", "GHMC ఆస్తి పన్ను ఎర్లీ బర్డ్ రాయితీ: ఈ ఏడాది చివరి తేదీ చూడండి"),
    (6, 1, "🦟", "Monsoon is coming: keep mosquito nets and repellent ready", "వర్షాకాలం వస్తోంది: దోమతెరలు, దోమల మందు సిద్ధంగా ఉంచండి"),
    (7, 31, "🧾", "Income tax return due date (if you file a return)", "ఆదాయపు పన్ను రిటర్న్ చివరి తేదీ (మీరు రిటర్న్ వేస్తే)"),
    (9, 15, "💉", "Ask your doctor about this year's flu vaccine", "ఈ ఏడాది ఫ్లూ టీకా గురించి డాక్టర్‌ను అడగండి"),
    (10, 1, "📜", "Life certificate opens for pensioners aged 80 and above", "80 ఏళ్లు పైబడిన పెన్షనర్లకు లైఫ్ సర్టిఫికేట్ మొదలు"),
    (11, 1, "📜", "Life certificate month for all pensioners begins", "అందరు పెన్షనర్లకు లైఫ్ సర్టిఫికేట్ నెల మొదలు"),
    (11, 30, "⏰", "Last day to submit your life certificate", "లైఫ్ సర్టిఫికేట్ ఇవ్వడానికి చివరి రోజు"),
]

# (icon, test, Telugu test, how often, Telugu how often)
CHECKUPS = [
    ("🩸", "Blood pressure", "బీపీ (రక్తపోటు)", "At least every 6 months; monthly if you have BP", "కనీసం 6 నెలలకు ఒకసారి; బీపీ ఉంటే ప్రతి నెల"),
    ("🍬", "Blood sugar (HbA1c)", "షుగర్ (HbA1c)", "Every year; every 3 months if you have diabetes", "ప్రతి సంవత్సరం; షుగర్ ఉంటే ప్రతి 3 నెలలకు"),
    ("🫀", "Cholesterol (lipid profile)", "కొలెస్ట్రాల్ (లిపిడ్ ప్రొఫైల్)", "Every year", "ప్రతి సంవత్సరం"),
    ("🧪", "Kidney tests (creatinine, urine)", "కిడ్నీ పరీక్షలు (క్రియాటినిన్, మూత్రం)", "Every year, especially with diabetes or BP", "ప్రతి సంవత్సరం, ముఖ్యంగా షుగర్ లేదా బీపీ ఉంటే"),
    ("👁️", "Eyes (cataract, glaucoma)", "కళ్ళు (కంటిశుక్లం, గ్లాకోమా)", "Every year", "ప్రతి సంవత్సరం"),
    ("👂", "Hearing", "వినికిడి", "Every year", "ప్రతి సంవత్సరం"),
    ("🦷", "Teeth and gums", "పళ్ళు, చిగుళ్ళు", "Every 6 months", "ప్రతి 6 నెలలకు"),
    ("🦴", "Bone strength (DEXA scan)", "ఎముకల బలం (DEXA స్కాన్)", "Once after 65 for women and after 70 for men, then as your doctor advises", "మహిళలకు 65 తర్వాత, పురుషులకు 70 తర్వాత ఒకసారి, ఆ తర్వాత డాక్టర్ చెప్పినట్లు"),
    ("🎗️", "Cancer screening (breast, cervix, colon, mouth)", "క్యాన్సర్ పరీక్షలు (రొమ్ము, గర్భాశయ ముఖద్వారం, పెద్దపేగు, నోరు)", "Ask your doctor which ones and how often", "ఏవి, ఎంత తరచుగా అనేది డాక్టర్‌ను అడగండి"),
    ("💉", "Vaccines (flu, pneumonia, tetanus)", "టీకాలు (ఫ్లూ, న్యుమోనియా, టెటనస్)", "Flu every year; others as your doctor advises", "ఫ్లూ ప్రతి సంవత్సరం; మిగతావి డాక్టర్ చెప్పినట్లు"),
    ("🦶", "Feet check", "పాదాల పరీక్ష", "At every doctor visit if you have diabetes", "షుగర్ ఉంటే ప్రతి డాక్టర్ సందర్శనలో"),
]

# Scam warning signs: (pattern, weight, English reason, Telugu reason)
SCAM_RULES = [
    (r"\b(otp|pin|cvv|password|passcode)\b|ఓటీపీ|పిన్|పాస్‌వర్డ్", 3,
     "Asks for an OTP, PIN, CVV or password. No bank or office ever asks for these.",
     "OTP, PIN, CVV లేదా పాస్‌వర్డ్ అడుగుతోంది. ఏ బ్యాంకు, కార్యాలయం వీటిని అడగదు."),
    (r"digital arrest|\barrest|\bcbi\b|\bwarrant\b|\bcourt\b|customs|narcotics|money laundering|అరెస్ట్|పోలీస్|కోర్టు", 3,
     "Threatens arrest or police action. Real police never arrest anyone by phone or video call.",
     "అరెస్ట్ లేదా పోలీసు చర్య అని బెదిరిస్తోంది. నిజమైన పోలీసులు ఫోన్ లేదా వీడియో కాల్‌లో అరెస్ట్ చేయరు."),
    (r"anydesk|teamviewer|quick ?support|screen ?shar|rustdesk", 3,
     "Asks you to install a screen-sharing app. This lets them control your phone.",
     "స్క్రీన్ షేరింగ్ యాప్ ఇన్‌స్టాల్ చేయమంటోంది. దీనితో వాళ్ళు మీ ఫోన్‌ను నియంత్రించగలరు."),
    (r"\bkyc\b|(account|card|sim|pension).{0,30}(block|suspend|close|deactivat|stop)|కేవైసీ|బ్లాక్", 2,
     "Says your account, card, SIM or pension will be blocked. Banks do not do this by SMS or call.",
     "మీ ఖాతా, కార్డు, సిమ్ లేదా పెన్షన్ బ్లాక్ అవుతుందని చెబుతోంది. బ్యాంకులు SMS లేదా కాల్ ద్వారా ఇలా చేయవు."),
    (r"electricity|power.{0,20}(cut|disconnect)|current bill|bill.{0,20}(pending|unpaid|due)|కరెంట్", 2,
     "Says your electricity will be cut. The power department does not send such messages from mobile numbers.",
     "కరెంట్ కట్ అవుతుందని చెబుతోంది. విద్యుత్ శాఖ మొబైల్ నంబర్ల నుండి అలాంటి సందేశాలు పంపదు."),
    (r"lottery|\bprize|you (have )?won|winner|reward|cash ?back|\bgift\b|లాటరీ|బహుమతి", 2,
     "Promises a prize, lottery or reward. You cannot win a contest you never entered.",
     "బహుమతి, లాటరీ లేదా రివార్డ్ వచ్చిందని చెబుతోంది. మీరు పాల్గొనని పోటీలో గెలవలేరు."),
    (r"https?://|www\.|bit\.ly|tinyurl|\.apk\b", 2,
     "Contains a link or app file. Do not open links in unexpected messages.",
     "లింక్ లేదా యాప్ ఫైల్ ఉంది. అనుకోని సందేశాల్లోని లింక్‌లు తెరవకండి."),
    (r"work from home|part[- ]?time job|double your money|guaranteed return|stock tips|crypto|telegram group|పెట్టుబడి|రెట్టింపు", 2,
     "Offers easy money, a part-time job or guaranteed investment returns.",
     "సులభంగా డబ్బు, పార్ట్ టైమ్ ఉద్యోగం లేదా గ్యారంటీ లాభం ఇస్తామంటోంది."),
    (r"accident|in hospital|your (son|daughter|grandson|granddaughter)|ప్రమాదం|మీ (కొడుకు|కూతురు|మనవడు)", 2,
     "Says a family member is in trouble and needs money. Call that person directly first.",
     "కుటుంబ సభ్యుడు ఇబ్బందిలో ఉన్నాడని, డబ్బు కావాలని చెబుతోంది. ముందుగా ఆ వ్యక్తికి మీరే నేరుగా కాల్ చేయండి."),
    (r"(call|contact|whatsapp)\D{0,15}\b[6-9][\dx]{9}\b|\b[6-9][\dx]{9}\D{0,6}(కి|కు) కాల్", 2,
     "Asks you to call a private mobile number. Use only the number printed on your bill, card or passbook.",
     "ఒక ప్రైవేట్ మొబైల్ నంబర్‌కు కాల్ చేయమంటోంది. మీ బిల్లు, కార్డు లేదా పాస్‌బుక్‌పై ఉన్న నంబర్‌నే వాడండి."),
    (r"(do not|don't|dont) tell (anyone|anybody|your family)|keep (this|it) (a )?secret|ఎవరికీ చెప్పకండి|రహస్యంగా", 2,
     "Tells you to keep it secret. Scammers do not want you to ask your family.",
     "రహస్యంగా ఉంచమంటోంది. మీరు కుటుంబాన్ని అడగకూడదని మోసగాళ్లు ఇలా చెబుతారు."),
    (r"urgent|immediately|right now|tonight|today itself|ఈ రాత్రి|within \d+ (hours?|minutes?|mins?)|last chance|act now|వెంటనే|ఈ రోజే|అత్యవసరం", 1,
     "Pushes you to act in a hurry. Scammers do not want you to stop and think.",
     "తొందరపెడుతోంది. ఆలోచించే సమయం ఇవ్వకూడదని మోసగాళ్లు ఇలా చేస్తారు."),
    (r"\bupi\b|transfer|send money|processing fee|refund|deposit|pay now|డబ్బు పంప|ఫీజు", 1,
     "Asks you to send or pay money.",
     "డబ్బు పంపమని లేదా చెల్లించమని అడుగుతోంది."),
]

BLOOD_GROUPS = ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
