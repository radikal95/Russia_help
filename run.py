#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import telebot
import config
from db_tool import DbQuery

db_query = DbQuery()

bot = telebot.TeleBot(config.token)

def stage_check(message):
    query = """SELECT stage
        	        FROM public."user"
                    WHERE id={};"""
    query_result = db_query.execute_query(query.format(message.chat.id))
    if len(query_result.value) < 1:
        return None
    else:
        return query_result.value[0][0]
def login_check(message):
    query = """SELECT auth
    	        FROM public."user"
                WHERE id={};"""
    query_result = db_query.execute_query(query.format(message.chat.id))
    if len(query_result.value)<1:
        return False
    else:
        return query_result.value[0][0]
def update_name(message):
    query = """UPDATE public."user"
            SET full_name_provided ='{}', stage=2
            WHERE id={};"""
    query_result =  db_query.execute_query(query.format(message.text, message.chat.id), is_dml=True)
    if query_result.success:
        bot.send_message(message.chat.id,"Got it! Now tell us what is your office?")
def update_office(message):
    query = """UPDATE public."user"
                SET office ='{}', stage=3
                WHERE id={};"""
    query_result = db_query.execute_query(query.format(message.text, message.chat.id), is_dml=True)
    if query_result.success:
        bot.send_message(message.chat.id,"Got it! Now we are ready to help you!\nPress /menu to start")

@bot.message_handler(commands=['start'])
def insert_into_a_db(message):
    query = """SELECT auth
	        FROM public."user"
            WHERE id={};"""
    query_result=db_query.execute_query(query.format(message.chat.id))
    if len(query_result.value)<1:
        query ="""INSERT INTO public."user"
        (id, full_name_telegram,stage,auth)
        VALUES ({},'{}',{}, False);"""
        name = 'Unknown user'
        if message.chat.first_name:
            name = str(message.chat.first_name)
        if message.chat.last_name:
            name = name + ' ' + str(message.chat.last_name)
        query_result=db_query.execute_query(query.format(message.chat.id,name,0),is_dml=True)
        if (query_result.success):
            bot.send_message(message.chat.id, "So, tell us the key")
    else:
        if not query_result.value[0][0]:
            bot.send_message(message.chat.id, "Tell us the key")
        else:
            bot.send_message(message.chat.id, "Press /menu for to start!")

@bot.message_handler(regexp=config.secret_key)
def login(message):
    print('a')
    query = """SELECT auth
    	        FROM public."user"
                WHERE id={};"""
    query_result = db_query.execute_query(query.format(message.chat.id))
    if len(query_result.value)<1:
        bot.send_message(message.chat.id, "You are not authorized")
    else:
        if not query_result.value[0][0]:
            query = """UPDATE public."user"
                    SET auth = true, stage=1
                    WHERE id={};"""
            query_result=db_query.execute_query(query.format(message.chat.id),is_dml=True)
            print(query_result)
            if query_result.success:
                bot.send_message(message.chat.id, "<b>The password is correct!</b> \n"
                "Please, answer some simple questions. \nWhat is your name?""", parse_mode='HTML')
        else:
            bot.send_message(message.chat.id,
"""/schedule - schedule information \n
/tickets - security information \n
/visa - visa information \n
/accommodation - accommodation and hotels \n
/taxi - taxi \n
/fan_id - all about fan id \n
/security - security information \n
/travel - sightseeing or entertainment information \n
/office - office ivents information""")

@bot.message_handler(regexp='/menu')
def menu(message):
    bot.send_photo(message.chat.id, photo=open('1.jpg', 'rb'), caption=
                   "For the first time in history, Russia is hosting the FIFA World Cup on June 14 - July 15!")
    bot.send_message(message.chat.id,
"Moscow office welcomes McKinsey football fans from around the world and provide support to make your stay in Russia exciting and safe.\n\n"
"<b>To get assistance with visa/travel/hotel booking send your request to our Travel Support Desk to</b> FIFA2018-Travel@mckinsey.com \n\n"
"<b>FAQ</b>\n\n"
"<b>1. What is FIFA World Cup schedule and hosting cities in Russia?</b> \n- /schedule \n"
"<b>2. How to purchase match tickets?</b> - /tickets \n"
"<b>3. How to get Russian visa or/and FAN ID?</b> - /visa \n"
"<b>4. How to find accommodations and obtain temporary residence registration?</b> - /accommodation \n"
"<b>5. How to arrange taxi transfer in Russia?</b> - /taxi \n"
"<b>6. What are security recommendations and emergency contacts?</b> - /security \n"
"<b>7. What are the top places/sightseeing to visit?</b> - /travel \n"
"<b>8. How to attend Moscow office events?</b> - /office \n",
parse_mode='HTML')


@bot.message_handler(func=lambda message: login_check(message))
def dialog(message):
    stage = stage_check(message)
    # Normal work
    if stage==3:
        if message.text == '/schedule':
            bot.send_message(message.chat.id,
                             "2018 FIFA World cup will take place in 11 Russian cities: \n"
                             "Volgograd, Ekaterinburg, Kazan, Kaliningrad, Moscow, Nizhny Novgorod, Rostov-on-Don, Samara, Saint-Petersburg, Saransk and Sochi \n"
                             "from June 14, 2018 till July 15, 2018\n"
                             "Find detailed schedule <a href='http://www.fifa.com/worldcup/matches/index.html'>here</a>\n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/tickets':
            bot.send_message(message.chat.id,
                             "The World Cup tickets are made available in 3 sales phases. Currently, <b>the third sales phase</b> is taking place, which consists of random selection draw period and the first come first served basis.\n\n"
                             "<b>The first come first served sales period takes place from 13 March to 03 April.</b> Available tickets are allocated directly to the Ticket Applicants. <b>The last minute sales phase</b> will take place <b>from 18 April to 15 June.</b> \n\n"
                             "Note that <a href='FIFA.com/tickets'>FIFA.com</a> is the exclusive sales channel for all ticket sales to the general public.\n"
                             "\n<b>IMPORTANT:</b> Any tickets obtained from any other sources (unauthorized intermediaries such as ticket brokers, internet auctions, internet ticket agents, or unofficial ticket exchange platforms) will be automatically cancelled once identified.\n\n"
                             "<b>Useful links:</b>\n"
                             + u'\U0001F4CD' + "<a href='http://www.fifa.com/worldcup/organisation/ticketing/index.html'>Ticketing</a> \n"
                             + u'\U0001F4CD' + "Official FIFA World Cup ticket center <a href='https://support.tickets.fifa.com/en-gb/enquiry-form.aspx'>Hot Line</a>: + 41 44 563 2018 (for foreign residents)\n"
                             + u'\U0001F4CD' + "<a href='https://tickets.fifa.com/FAQ/en?platform=desktop&lang=en'>FAQ</a>\n\n"
                                               "You can also buy ticket-inclusive hospitality packages, each one offering its own unique hospitality experience and service levels though the price will be significantly higher than average.\n"
                             + u'\U0001F4CD' + "Visit the <a href='https://hospitality.fifa.com/hospitality2018/hospitality-packages/emotional-home'>website</a>\n"
                             + u'\U0001F4CD' + "Find your regional <a href='https://hospitality.fifa.com/hospitality2018/sales-appointed-agents'>sales agents</a>\n\n"
                                               "To return press /menu",
                             parse_mode='HTML')
        elif message.text == '/visa':
            bot.send_message(message.chat.id,
                             "<b> How to get Russian visa or / and FAN ID? </b> \n\n"
                             "What does visa-free regime for FAN ID holders mean? - /free \n"
                             "What is FAN ID and how can I get it? - /fan_id \n"
                             "Which details do I need to provide for a FAN ID? - /details \n"
                             "How I can receive FAN ID once it is ready?	- /receive \n"
                             "FAQ - /faq\n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/free':
            bot.send_message(message.chat.id,
                             "Russia has introduced special entry rules for the <a href='https://en.wikipedia.org/wiki/2018_FIFA_World_Cup'>2018 FIFA World Cup</a> participants and fans. According to these rules, fans are entitled to multiple visa-free entry <b>from 04 June to 25 July 2018</b>.\n"
                             "You need to obtain the FAN ID after you have bought your tickets or received confirmation for a ticket to a 2018 World Cup match. For the <b>visa-free entry</b> you will need to show your <b>FAN ID</b> and a valid identity document recognized as such by the Russian authorities (e.g. international passport). Please note, that a FAN ID will be also required to leave Russia once it had been used for visa-free entry purposes.\n\n"
                             "To return press /menu",
                             parse_mode='HTML')
        elif message.text == '/fan_id':
            bot.send_message(message.chat.id,
                             "A FAN ID is your personal identification document for the 2018 FIFA World Cup. You must have your FAN ID (and a valid ticket) with you to access stadiums. FAN IDs are issued free of charge.\n\n"
                             "FAN IDs are mandatory for all 2018 FIFA World Cup spectators including Russian residents and children of all ages.\n\n"
                             "FAN ID also entitles you to the free use of public transport on match days in the host cities.\n\n"
                             "In order to receive the FAN ID, please fill out and submit your application on www.fan-id.ru or contact one of the FAN ID Distribution centers in any of the host cities.\n\n"
                             "<b>IMPORTANT:</b>\n\n"
                             "During the application process for your FAN ID, you must specify the details from the same identity document that you will use for entry into the Russian Federation."
                             "If you already have a Russian visa valid within the <a href='https://en.wikipedia.org/wiki/2018_FIFA_World_Cup'>2018 FIFA World Cup</a> period, you still need to apply for a FAN ID in advance to access the stadiums.\n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/details':
            bot.send_message(message.chat.id,
                             "To fill out the application for a FAN ID, you will need to submit the following data:\n"
                             "- Last name, given name, patronymic (second name or names);\n"
                             "- Date of birth;\n"
                             "- Gender;\n"
                             "- Details of your identity document (document type, number, issuing authority and date of issue);\n"
                             "- Citizenship;\n"
                             "- Ticket request number or a 2018 FIFA World Cup match ticket number;\n"
                             "- Photo;\n"
                             "- Mobile phone number;\n"
                             "- E-mail address;\n"
                             "- Mail address for FAN ID delivery.\n\n"
                             "To return press /menu")
        elif message.text == '/receive':
            bot.send_message(message.chat.id,
                             "You can choose postal delivery or delivery through the VFS Global Visa Application centers located outside Russia.\n\n"
                             "<b>1. Postal delivery </b> \n\n"
                             "The average estimated delivery time for a FAN ID to a foreign country is about 30 days. It usually takes 7 to 11 days for a package to cross the Russian border. Please check the delivery time of your local postal operator and add up these periods in order to estimate your delivery period.\n\n"
                             "<b>2. Delivery through Global Visa Applicant centers</b>\n\n"
                             "The estimated delivery time for a FAN ID to a foreign country is about 30 days.\n\n"
                             "You can track your FAN ID delivery on the VFS <a href='www.vfsglobal.com'>website</a>\n\n"
                             "To return press /menu",
                             parse_mode='HTML')
        elif message.text == '/faq':
            bot.send_message(message.chat.id,
                             "<b>WHAT IF...</b>\n\n"
                             u'\U0001F4CD'"<b>I have a valid Russian visa and do not have FAN ID</b>\n\n"
                             "You can enter Russia for business, work, tourism, or private purposes depending on your visa type.\n"
                             "You still need to apply for a FAN ID if you want to access the stadiums. With a valid Russian visa you can either get your FAN ID in advance at your home country or visit the one of distribution centers located in the host cities upon your arrival to Russia.\n\n"
                             "You do not need to apply for a FAN ID if you are not going to access the stadiums.\n\n"
                             u'\U0001F4CD' "<b>I have FAN ID and do not have a valid Russian visa</b>\n\n"
                             "You can enter Russia without a visa within the period starting 10 days before the first match and 10 days after the final match, which is <b>from 04 June to 25 July 2018</b>, by providing your FAN ID and a valid passport (or any other valid identity document recognized by the Russian Federation).\n\n"
                             u'\U0001F4CD' "<b>I will visit Russia as a tourist and may visit 2018 FIFA World Cup matches</b>\n\n"
                             "You can enter Russia as a tourist in accordance with your visa type.\n\n"
                             "You still need to apply for a FAN ID if you want to access the stadiums. You can visit the one of distribution centers located in the host cities and get a FAN ID while you are in Russia by providing the tickets for the match.\n\n"
                             "You do not need to apply for a FAN ID if you are not going to access the stadiums.\n\n"
                             "To return press /menu",
                             parse_mode="HTML")
        elif message.text == '/accommodation':
            bot.send_message(message.chat.id,
                             "We kindly advise you to book your accommodation well in advance as hotel options will be sold out very quickly. During the FIFA World Cup special rates and conditions are applicable:\n\n"
                             "- No corporate rates are available \n"
                             "- Minimum stay from 4 nights \n"
                             "- Non-refundable \n"
                             "- 100% Prepaid \n\n"
                             "<b>To get assistance with hotel booking contact our Travel Support Desk on</b> FIFA2018-Travel@mckinsey.com\n\n"
                             "In accordance with the special migration regime introduced in Russia during the 2018 FIFA World Cup, all foreign nationals need to register within 24 hours upon arrival, instead of 7 working days normally. This rule applies to Volgograd, Ekaterinburg, Kazan, Kaliningrad, Moscow, Nizhny Novgorod, Rostov-on-Don, Samara, Saint-Petersburg, Saransk and Sochi from May 25, 2018 till July 25, 2018.\n\n"
                             "If you are travelling between the host cities, you need to register each time upon arrival to every city and submit the registration card you obtained in the previous city.\n\n"
                             "According to the law, either you or your receiving party (i.e. your hotel or host) need to get the registration in the territorial department of the Ministry of Internal Affairs.\n\n"
                             "All territorial departments will be working 7 days a week during the World Cup. Registrations via Russian Post or multifunctional centers are not allowed.\n\n"
                             "<b>Staying in a hotel:</b>\n\n"
                             "If you are staying in a hotel, your hotel is responsible for your registration.\n\n"
                             "<b>Staying in a private apartment:</b>\n\n"
                             "If you are staying in a private house or an apartment, the host will need to register you at the territorial department of the Ministry of Internal Affairs.\n\n"
                             "<a href='http://welcome2018.com/en/journal/materials/v-gorodakh-kk-2017-izmenen-poryadok-registratsii-po-mestu-prebyvaniya/'>More info</a>\n\n"
                             "To return press /menu",
                             parse_mode="HTML")
        elif message.text == '/taxi':
            bot.send_message(message.chat.id,
                             "Full list of preferred corporate taxi companies in Russia is <a href='http://moscow.intranet.mckinsey.com/taxi'>here</a> \n\n"
                             "<b>NOTE:</b> Yandex.Taxi currently available only with Russian sim card.\n\n"
                             "To return press /menu",
                             parse_mode='HTML')
        elif message.text == '/security':
            bot.send_message(message.chat.id,
                             "McKinsey Moscow Office works closely with Firm security and Russian authorities to ensure your safe stay in Russia. We are currently working with an external security firm to provide a special deal to get access to a security service (Hotline button) for all Firm members travelling to Russia at an affordable cost. Detailed information <b>will be available in May.</b>\n\n"
                             "All locations have normal levels of street crime associated with big cities; \n\n"
                             "All host cities have good accommodation and medical facilities; \n\n"
                             "The most common problems visitors are likely to experience are petty theft and street crime – as in any large city.\n\n"
                             "<b>List of recommended hospitals by International SOS in the WC host cities:</b>\n\n"
                             "Moscow - /moscow \n"
                             "Saint Petersburg - /saint_petersburg \n"
                             "Kaliningrad - /kaliningrad \n"
                             "Nizhny Novgorod - /nizhny_novgorod \n"
                             "Samara - /samara \n"
                             "Ekaterinburg - /ekaterinburg \n"
                             "Kazan - /kazan \n"
                             "Volgograd - /volgograd \n"
                             "Sochi - /sochi \n "
                             "Saransk - /saransk \n"
                             "Rostov-on-Don - /rostov_on_don \n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/moscow':
            bot.send_message(message.chat.id,
                             "<b>Recommended Hospitals</b> \n\n"
                             "<b>GMS na Smolenskoy</b>\n"
                             "<b>Address</b>: 6 bld 1, 1st Nikolocshepovkyi pereulok, Moscow 121099 \n"
                             "<b>Tel (General)</b>: +7(495) 781 55 77 / +7(800) 302 55 77 \n"
                             "<b>Email</b>: mc@gmsclinic.ru \n"
                             "<b>Website</b>:  http://www.gmsclinic.com/ \n\n"
                             "<b>European Medical Center Schepkina</b> \n"
                             "<b>Address</b>: Schepkina street 35, Moscow 129090 \n"
                             "<b>Tel (General)</b>: +7(495) 933 66 55 \n"
                             "<b>Email</b>: cs@emcmos.ru \n"
                             "<b>Website</b>: http://www.emcmos.ru/en/main \n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/saint_petersburg':
            bot.send_message(message.chat.id,
                             "<b>Recommended Hospitals</b> \n\n"
                             "<b>Euromed Clinic</b>\n"
                             "<b>Address</b>: 60, Suvorovsky prospect, Saint Petersburg 191124 \n"
                             "<b>Tel (General)</b>: +7 (812) 327 03 01 \n"
                             "<b>Email</b>: euromed@euromed.ru  \n"
                             "<b>Website</b>: http://en.euromed.ru/en/ \n\n"
                             "<b>American Medical Clinic & Hospital</b> \n"
                             "<b>Address</b>: 78 Moika emb, Saint Petersburg 190000 \n"
                             "<b>Tel (General)</b>: +7 (812) 740 20 90 \n"
                             "<b>Email</b>: info@amclinic.ru \n"
                             "<b>Website</b>: http://www.amclinic.com/ \n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/kaliningrad':
            bot.send_message(message.chat.id,
                             "<b>Recommended Hospitals</b> \n\n"
                             "<b>Regional Clinical Hospital of Kaliningrad</b>\n"
                             "<b>Address</b>: 74, Klinicheskaya Street, Kaliningrad 236016 \n"
                             "<b>Tel (General)</b>: +7(401) 257 85 78 / +7(401) 257 86 78 / +7(401) 257 85 75 / +7(401) 257 86 97 \n"
                             "<b>Website</b>: http://www.kokb.ru/ \n\n"
                             "<b>Medical center MedExpert</b> \n"
                             "<b>Address</b>: 8, Podpolkovnika Ivannikova street, \n12 F.Leforta boulevard, \n1, Prazhskaya street, Kaliningrad 236040 \n"
                             "<b>Tel (General)</b>: +7(401) 256 77 22 / +7(401) 279 15 15 / +7(401) 256 77 44 \n"
                             "<b>Website</b>: http://www.med-expert.ru/ \n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/nizhny_novgorod':
            bot.send_message(message.chat.id,
                             "<b>Recommended Hospitals</b> \n\n"
                             "<b>Privolzhskiy Regional Medical Center</b>\n"
                             "<b>Address</b>: 2 NizhneVolzhskaya embankment, 14 Ilyinskaya street \n 20a Marshala Voronova street, Nizhniy Novgorod 603001 \n"
                             "<b>Tel (General)</b>: +7(831) 428 81 88 \n"
                             "<b>Website</b>:  http://www.pomc.ru/ \n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/samara':
            bot.send_message(message.chat.id,
                             "<b>Recommended Hospitals</b> \n\n"
                             "<b>First private clinic of Samara</b>\n"
                             "<b>Address</b>: 16, Yarmorochnaya Street, Samara 443001 \n"
                             "<b>Tel (General)</b>: +7 (846) 242 07 13 / +7 (846) 242 04 18 \n"
                             "<b>Website</b>:  http://www.fspc.ru/ \n\n"
                             "<b>Samara Regional Clinical Hospital named after Seredavin</b> \n"
                             "<b>Address</b>: 159, Tashkentskaya street, Samara 443095 \n"
                             "<b>Tel (General)</b>: +7 (846) 956 12 60 \n"
                             "<b>Website</b>: http://www.sokb.ru/ \n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/ekaterinburg':
            bot.send_message(message.chat.id,
                             "<b>Recommended Hospitals</b> \n\n"
                             "<b>Medical Association Novaya bolnitsa</b>\n"
                             "<b>Address</b>: 29, Zavodskaya street, Yekaterinburg 620109 \n"
                             "<b>Tel (General)</b>: +7(343) 355 56 57 \n"
                             "<b>Email</b>: a.nikitina@newhospital.ru \n"
                             "<b>Website</b>:  http://www.newhospital.ru/ \n\n"
                             "<b>European Medical Center UGMK-Zdorovie</b> \n"
                             "<b>Address</b>: 113, Sheikmana street, Yekaterinburg 620144 \n"
                             "<b>Tel (General)</b>: +7(343) 283 08 08 \n"
                             "<b>Email</b>: info@ugmk-clinic.ru  \n"
                             "<b>Website</b>: https://www.ugmk-clinic.ru/ \n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/kazan':
            bot.send_message(message.chat.id,
                             "<b>Recommended Hospitals</b> \n\n"
                             "<b>Republican Clinical Hospital of Tatarstan</b>\n"
                             "<b>Address</b>: Orenburgskiy tract, 138, Kazan 420064 \n"
                             "<b>Tel (General)</b>: +7(843) 231 20 90 \n"
                             "<b>Email</b>: plat.uslug@yandex.ru \n"
                             "<b>Website</b>: http://rkbrt.ru/ \n\n"
                             "<b>Clinic of Family Medicine, OOO</b> \n"
                             "<b>Address</b>: Yamasheva prospekt, 48B, Kazan 420103 \n"
                             "<b>Tel (General)</b>: +7(843) 211 10 11 \n"
                             "<b>Website</b>: http://www.ksm-kazan.ru/ \n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/volgograd':
            bot.send_message(message.chat.id,
                             "<b>Recommended Hospitals</b> \n\n"
                             "<b>Medical Center EMPO</b>\n"
                             "<b>Address</b>: Kalinina str., 13, 7th floor, Volgograd 400001 \n"
                             "<b>Tel (General)</b>: +7(844) 293 34 29 / +7(844) 293 37 51 \n"
                             "<b>Website</b>:  http://xn--l1aec8c.xn--p1ai/ \n\n"
                             "<b>Regional Clinical Hospital #1 of Volgograd</b> \n"
                             "<b>Address</b>: Angarskaya str., 13, Volgograd 400049 \n"
                             "<b>Tel (General)</b>: +7(844) 236 31 66 / +7(844) 236 30 46 \n"
                             "<b>Email</b>: vokb@vokb.net \n"
                             "<b>Website</b>: https://vokb1.ru/ \n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/sochi':
            bot.send_message(message.chat.id,
                             "<b>Recommended Hospitals</b> \n\n"
                             "<b>City hospital # 4 of Sochi</b>\n"
                             "<b>Address</b>:1, Tuapsinskaya street, Sochi 354057 \n"
                             "<b>Tel (General)</b>: +7(862) 261 42 30 / +7(862) 261 05 21 / +7(862) 291 77 03 (hotline 24/7) \n"
                             "<b>Website</b>:  http://www.xn--4-9sbfw3ar7b.xn--p1ai/ \n\n"
                             "<b>Armed</b> \n"
                             "<b>Address</b>: Gagarina street, 19A, Sochi 354000 \n"
                             "<b>Tel (General)</b>: +7(862) 254 55 55 \n"
                             "<b>Email</b>: dms_armed@mail.ru \n"
                             "<b>Website</b>: http://armed-mc.ru/en/ \n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/saransk':
            bot.send_message(message.chat.id,
                             "<b>Recommended Hospitals</b> \n\n"
                             "<b>Republican Clinical Hospital #4</b>\n"
                             "<b>Address</b>: 32, Ulyanova str, Saransk 430032 \n"
                             "<b>Tel (General)</b>: +7(834) 233 42 22 \n"
                             "<b>Website</b>: http://www.rkb4.ru/ \n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/rostov_on_don':
            bot.send_message(message.chat.id,
                             "<b>Recommended Hospitals</b> \n\n"
                             "<b>Rostovskaya Clinical Hospital of the FMBA</b>\n"
                             "<b>Address</b>: 6, Pervaya linia street - out-patient dept. \n 34, Peshkova street - in-patient dept. Rostov on Don 344019 \n"
                             "<b>Tel (General)</b>: +7(863) 254 81 44 / +7(863) 254 94 00  \n"
                             "<b>Email</b>: marketing@uomc-mail.ru \n"
                             "<b>Website</b>: http://www.umedcentr.ru/ \n\n"
                             "<b>Medical center Family</b> \n"
                             "<b>Address</b>: 8, Dachnaya street, Rostov on Don 344064 \n"
                             "<b>Tel (General)</b>: +7(863) 223 17 77 / +7(863) 223 24 77 / +7(863) 223 25 75 / +7(863) 223 24 25 / +7(863) 223 24 58 / +7(863) 223 25 77 \n"
                             "<b>Email</b>: info@mc-semya.ru \n"
                             "<b>Website</b>: http://mc-semya.ru/ \n\n"
                             "To return press /menu", parse_mode='HTML')
        elif message.text == '/travel':
            bot.send_message(message.chat.id,
                             "If you want to plan sightseeing or entertainment activities, we recommend using the following websites. \n\n"
                             "<a href='http://welcome2018.com/en/'>Fan guide</a> (available in English, German, French, Spanish and Russian) \n\n"
                             "Fan guide mobile app (available in English, German, French, Spanish and Russian via App stores): <b>Welcome 2018 </b> \n\n"
                             "Tap <a href='https://itunes.apple.com/ru/app/welcome-2018/id1178936802?l=en&mt=8'>here</a> for iOS \n\n"
                             "Tap <a href='https://play.google.com/store/apps/details?id=com.welcome2018'>here</a> for Android \n\n "
                             + u'\U0001F4CD' + "tripadvisor.com \n\n"
                             + u'\U0001F4CD' + "onelyplanet.com/russia \n\n"
                             + u'\U0001F4CD' + "timeout.com/ (for Moscow)\n\n"
                             + u'\U0001F4CD' + "afisha.yandex.com (for Moscow and St.Petersburg) \n\n"
                             + u'\U0001F4CD' + "moscow.inyourpocket.com \n\n"
                                               "To buy tickets to events:\n\n"
                             + u'\U0001F4CD' + "parter.ru/bilety.html?language=en\n\n"
                             + u'\U0001F4CD' + "Kassir.ru \n\n"
                             + u'\U0001F4CD' + "ticketland.ru\n\n"
                            "To return press /menu", parse_mode='HTML')
        elif message.text == '/office':
            bot.send_message(message.chat.id,
                             "To mark this momentous event, Moscow office invites you to: \n\n"
                             + u'\U0001F4CD' + "Happy hours with match broadcasts in June-July \n"
                             + u'\U0001F4CD' + "Friendly match 'Russia VS the World' in June 2nd half \n"
                             + u'\U0001F4CD' + "Summer rowing tournament in June-July \n\n"
                                               "Sign up to participate <a href='https://www.surveymonkey.com/r/V8DH32F'>here</a> \n\n"
                                               "Detailed information will follow. \n\n"
                                               "Stay up to date with the latest news from the Moscow office and get ready for this sensational event! \n\n"
                                               "To return press /menu",
                             parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "Can't find such command")
    # User name asked
    if stage==1:
        update_name(message)
    # Office name asked
    if stage==2:
        update_office(message)

@bot.message_handler(content_types='text')
def default_answer(message):
    bot.send_message(message.chat.id, "You are not authorized")

while True:
    try:
        bot.polling(none_stop=True)
    except:
        continue