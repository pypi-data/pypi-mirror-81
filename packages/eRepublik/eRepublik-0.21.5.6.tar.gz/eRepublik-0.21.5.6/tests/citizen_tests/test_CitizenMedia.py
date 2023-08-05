from erepublik.access_points import CitizenBaseAPI, ErepublikArticleAPI
from erepublik.citizen import CitizenMedia

from unittest import TestCase

import responses

from . import URL


class ArticleAPITests(TestCase):
    def setUp(self) -> None:
        self.api = CitizenMedia()

    @responses.activate
    def test_get_main_article_json(self):
        return
        article_id = 2719628
        responses.add(responses.GET, f'{URL}/main/articleJson/{article_id}', """{"newspaper":{"id":201132,"name":"Latvijas kara ministrija","countryId":71,"citizen":{"id":1954361,"name":"Kara ministrija","avatar":"https://cdnt.erepublik.net/PprbCpbo0QKr6y72kw5nesUmYxw=/55x55/smart/avatars/Citizens/2009/09/24/fc5e2a4431dcc690043a99c168116905.jpg"},"numArticles":1137,"subscribers":876,"isSubscribed":true,"canSubscribe":false,"prevArticle":{"id":2719336,"title":"[KM] Gaisa maizītes [d4585 00:09]"},"nextArticle":false},"articleData":{"articleId":2719628,"category":{"id":3,"name":"Warfare analysis"},"countryId":71,"createdAt":"yesterday","isEndorsed":100,"canEndorse":false,"endorsers":[{"citizenId":1620414,"amount":100,"name":"inpoc1","avatar":"https://cdnt.erepublik.net/cIKufNpt0oPgCEbyYWFOc1piEtw=/55x55/smart/avatars/Citizens/2009/07/08/4b57b9ebb0232f0d6c3f6f2c21b8ab95.png?b36adc7aded607be571e2404e0be6ef9"},{"citizenId":5365408,"amount":100,"name":"VASALS Bro","avatar":"https://cdnt.erepublik.net/kvH86QgVN11YzsMBip3KYA2qH-U=/55x55/smart/avatars/Citizens/2011/11/22/9966c6e1f0a7f058d32b31d596a7ccd4.jpg?55744011dcd62f084ce060fffdda4554"},{"citizenId":1607812,"amount":100,"name":"Oskara Kalpaks","avatar":"https://cdnt.erepublik.net/vuED-uPXUDHCTZQK9q-1vlhnBNg=/55x55/smart/avatars/Citizens/2009/07/04/6bddfd2147528cd7637fd398ba8c6e3f.jpg"}],"canVote":false,"isVoted":true,"numVotes":5,"numComments":7,"canComment":true,"canDelete":false,"canEdit":false,"isModerator":false},"article":{"title":"[KM] Gaisa maizītes [d4592 00:10]","body":"<div style=\"text-align:center\">\n<img src=\"https://dl.dropboxusercontent.com/s/hwezdgrhjvfecfx/KaraMinistrijasLogo.jpg\" class=\"bbcode_img\"><br><br><br><b>★★★★ GAISA MAIZĪTES ★★★★</b>\n</div>\n<br>\nIr noslēgusies 147. pilotu apgādes nedēļa.<br><br><u><b>UZMANĪBU</b> Sakarā ar to, ka pilotu apgādē obligāti nepieciešams lietot vismaz vienu māju, tad, ja izdales brīdī nav aktivizēta neviena māja, apgāde izpaliek un pretenzijas netiek izskatītas!</u><br>\nPilotu apgāde ir automatizēta, ja pieteikums nav kā <u>atbildes komentārs uz Kara Ministrijas komentāru</u> un ja <u>komentārs nesatur \"piesakos\"</u> (lielie mazie burti nav svarīgi), tad apgāde var izpalikt un pretenzijas netiks izskatītas.<br><br><br><b><u>* Atcerieties, lietojiet Q1 mājiņas, tā ir obligāta prasība!</u></b><br><br><br><b>Nedēļas apkopojums:</b><br><br>\nPieteicās 5 spēlētaji:<br><table><tbody><tr><td>\n<b>Spēlētajs</b><br><b><a href=\"https://www.erepublik.com/en/citizen/profile/9476097\">LStars</a></b><br><b><a href=\"https://www.erepublik.com/en/citizen/profile/5365408\">VASALS Bro</a></b><br><b><a href=\"https://www.erepublik.com/en/citizen/profile/4360535\">aigarsjo</a></b><br><b><a href=\"https://www.erepublik.com/en/citizen/profile/9533135\">Stikene</a></b><br><b><a href=\"https://www.erepublik.com/en/citizen/profile/1607812\">Oskara Kalpaks</a></b>\n</td><td>\n<b>Kilu skaits</b><br>\n1024<br>\n639<br>\n944<br>\n429<br>\n100\n</td><td>\n\n<div style=\"text-align:right\">\n<b>Enerģija</b><br>\n20 480<br>\n19 170<br>\n18 880<br>\n8 580<br>\n3 000\n</div>\n\n</td><td>\n\n<div style=\"text-align:center\">\n<b>7 DO</b><br>\n+<br>\n+<br>\n-<br>\n-<br>\n-\n</div>\n\n</td><td>\n\n<div style=\"text-align:center\">\n<b>Fabrikas</b><br>\n+<br>\n+<br>\n+<br>\n+<br>\n+\n</div>\n\n</td><td>\n\n<div style=\"text-align:right\">\n<b>Enerģija kopā</b><br>\n44 460<br>\n41 840<br>\n37 760<br>\n17 160<br>\n6 000\n</div>\n\n</td></tr></tbody></table><br><i>Atgādinājums visiem - pieteikties var līdz WC rangam, bet sākot ar CMS tiek kompensēti 20hp par katru kilu</i><br><br><b>★ Nedēļas sākumā enerģijas uzkrājums 0 enerģijas.<br>\n★ Kopā iztērēti 33566.72cc pārtikas iegādē.<br>\n★ Kopā šonedēļ izdalīts enerģijas apjoms 147220 enerģijas.<br>\n★ Enerģijas uzkrājums uz nākamo nedēļu - 0 enerģijas.</b><br><br><br><b>MAIZES APGĀDEI UZ NĀKAMO NEDĒĻU PIESAKĀMIES ŠAJĀ RAKSTĀ ZEM KARA MINISTRIJAS KOMENTĀRA, AR NORĀDI - piesakos!.<br>\nJa pieteikumā nebūs norādīts vārds \"piesakos\", tad uz apgādi var netikt pieskaitīts!</b><br><br><img src=\"https://dl.dropboxusercontent.com/s/y30q3d4ymeenzfa/Atdalitajs.png\" class=\"bbcode_img\"><br><br><b>Prasības pārtikas pretendentiem:</b><br><br>\n★ Latvietis sirdī un pēc pases - jābūt mūsu valsts pilsonim.<br><b>★ Aircraft rank līdz Wing Commander (neieskaitot) (līdz 1'673'000 aircraft rank points).</b><br>\n★ Pilotam ir jāpiesakās uz pārtiku KM raksta komentāros, kurā tiek izziņots par maizes apgādi tekošajai nedēļai.<br>\n★ Izdarīto kilu apjomam jābūt apskatāmam nedeļas valsts top 100 statistikā.<br><br>\nPēc pieprasījuma saņemšanas KM komanda izskata pieprasījumu, tiek pārbaudīts nedēļas laikā izdarītais kilu skaits gaisa kaujās. Nedēļas laikā izdarīto kilu skaitu reizinam ar <b>30, ja gaisa rangs līdz Chief Master Sergeant, bet sākot ar Chief Master Sergeant 20</b>, kas arī būs enerģijas apjoms, ko valsts kompensē jaunajam pilotam.<br><br><b>Papildu nosacījumi un pateicības atrodami <a href=\"https://www.erepublik.com/en/article/2712063\">šeit</a></b><br><br>\n- KM labprāt sagaida arī pārtikas ziedotājus.<br>\n- Pārtikas ziedotāju saraksts, pārtikas izlietojums tiks publicēts KM avīzē, rakstā, kurā piesakās pārtikai.<br><br><img src=\"https://dl.dropboxusercontent.com/s/y30q3d4ymeenzfa/Atdalitajs.png\" class=\"bbcode_img\"><br><br>\nAtceramies:<br>\nVisi Endorsers aizies pilotu apgādēm.<br><b>Tā kā lasām, ziedojam, atbalstām un karojam!</b><br><br><img src=\"https://dl.dropboxusercontent.com/s/y30q3d4ymeenzfa/Atdalitajs.png\" class=\"bbcode_img\"><br><br>\nAktuālie kauju paziņojumi tiek izziņoti:<br>\n* eLatvijas laika joslā (erepublik)<br>\n* <a href=\"//www.erepublik.com/en/main/warn/aHR0cHM6Ly9kaXNjb3JkYXBwLmNvbS9pbnZpdGUvV3dGNWgyMw==\"><b>eLatvijas Discord serverī</b></a> #valdības_paziņojumi<br><br><img src=\"https://dl.dropboxusercontent.com/s/y30q3d4ymeenzfa/Atdalitajs.png\" class=\"bbcode_img\"><br><br>\nApgādi veica: <b><a href=\"https://www.erepublik.com/en/citizen/profile/1620414\">inpoc1</a></b><br><br><br><div style=\"text-align:center\">\n<a href=\"https://www.erepublik.com/en/newspaper/187543/1\"><img src=\"https://dl.dropboxusercontent.com/s/34u16bcgfdsly2d/EkonomikasMinistrija.jpg\" class=\"bbcode_img\"></a><a href=\"https://www.erepublik.com/en/newspaper/201132\"><img src=\"https://dl.dropboxusercontent.com/s/gr9u0hfmk3j2ykt/KaraMinistrija.jpg\" class=\"bbcode_img\"></a><a href=\"https://www.erepublik.com/en/newspaper/207943\"><img src=\"https://dl.dropboxusercontent.com/s/650f20nxo3fkaxz/LabklajibasMinistrija.jpg\" class=\"bbcode_img\"></a><a href=\"https://www.erepublik.com/en/newspaper/220672\"><img src=\"https://dl.dropboxusercontent.com/s/j7kr1ebcd6fwylu/ValstsKanceleja.jpg\" class=\"bbcode_img\"></a><a href=\"https://www.erepublik.com/en/newspaper/235010\"><img src=\"https://dl.dropboxusercontent.com/s/1cjdt91ytnbplri/ArlietuMinistrija.jpg\" class=\"bbcode_img\"></a><a href=\"https://www.erepublik.com/en/newspaper/190402\"><img src=\"https://dl.dropboxusercontent.com/s/41dlgh2j6vv53pd/IzglitibasMinistrija.jpg\" class=\"bbcode_img\"></a>\n</div>"}}""")
        resp_json = self.api._get_main_article_json(article_id).json()

        self.assertEqual(resp_json, """{"newspaper":{"id":201132,"name":"Latvijas kara ministrija","countryId":71,"citizen":{"id":1954361,"name":"Kara ministrija","avatar":"https://cdnt.erepublik.net/PprbCpbo0QKr6y72kw5nesUmYxw=/55x55/smart/avatars/Citizens/2009/09/24/fc5e2a4431dcc690043a99c168116905.jpg"},"numArticles":1137,"subscribers":876,"isSubscribed":true,"canSubscribe":false,"prevArticle":{"id":2719336,"title":"[KM] Gaisa maizītes [d4585 00:09]"},"nextArticle":false},"articleData":{"articleId":2719628,"category":{"id":3,"name":"Warfare analysis"},"countryId":71,"createdAt":"yesterday","isEndorsed":100,"canEndorse":false,"endorsers":[{"citizenId":1620414,"amount":100,"name":"inpoc1","avatar":"https://cdnt.erepublik.net/cIKufNpt0oPgCEbyYWFOc1piEtw=/55x55/smart/avatars/Citizens/2009/07/08/4b57b9ebb0232f0d6c3f6f2c21b8ab95.png?b36adc7aded607be571e2404e0be6ef9"},{"citizenId":5365408,"amount":100,"name":"VASALS Bro","avatar":"https://cdnt.erepublik.net/kvH86QgVN11YzsMBip3KYA2qH-U=/55x55/smart/avatars/Citizens/2011/11/22/9966c6e1f0a7f058d32b31d596a7ccd4.jpg?55744011dcd62f084ce060fffdda4554"},{"citizenId":1607812,"amount":100,"name":"Oskara Kalpaks","avatar":"https://cdnt.erepublik.net/vuED-uPXUDHCTZQK9q-1vlhnBNg=/55x55/smart/avatars/Citizens/2009/07/04/6bddfd2147528cd7637fd398ba8c6e3f.jpg"}],"canVote":false,"isVoted":true,"numVotes":5,"numComments":7,"canComment":true,"canDelete":false,"canEdit":false,"isModerator":false},"article":{"title":"[KM] Gaisa maizītes [d4592 00:10]","body":"<div style=\"text-align:center\">\n<img src=\"https://dl.dropboxusercontent.com/s/hwezdgrhjvfecfx/KaraMinistrijasLogo.jpg\" class=\"bbcode_img\"><br><br><br><b>★★★★ GAISA MAIZĪTES ★★★★</b>\n</div>\n<br>\nIr noslēgusies 147. pilotu apgādes nedēļa.<br><br><u><b>UZMANĪBU</b> Sakarā ar to, ka pilotu apgādē obligāti nepieciešams lietot vismaz vienu māju, tad, ja izdales brīdī nav aktivizēta neviena māja, apgāde izpaliek un pretenzijas netiek izskatītas!</u><br>\nPilotu apgāde ir automatizēta, ja pieteikums nav kā <u>atbildes komentārs uz Kara Ministrijas komentāru</u> un ja <u>komentārs nesatur \"piesakos\"</u> (lielie mazie burti nav svarīgi), tad apgāde var izpalikt un pretenzijas netiks izskatītas.<br><br><br><b><u>* Atcerieties, lietojiet Q1 mājiņas, tā ir obligāta prasība!</u></b><br><br><br><b>Nedēļas apkopojums:</b><br><br>\nPieteicās 5 spēlētaji:<br><table><tbody><tr><td>\n<b>Spēlētajs</b><br><b><a href=\"https://www.erepublik.com/en/citizen/profile/9476097\">LStars</a></b><br><b><a href=\"https://www.erepublik.com/en/citizen/profile/5365408\">VASALS Bro</a></b><br><b><a href=\"https://www.erepublik.com/en/citizen/profile/4360535\">aigarsjo</a></b><br><b><a href=\"https://www.erepublik.com/en/citizen/profile/9533135\">Stikene</a></b><br><b><a href=\"https://www.erepublik.com/en/citizen/profile/1607812\">Oskara Kalpaks</a></b>\n</td><td>\n<b>Kilu skaits</b><br>\n1024<br>\n639<br>\n944<br>\n429<br>\n100\n</td><td>\n\n<div style=\"text-align:right\">\n<b>Enerģija</b><br>\n20 480<br>\n19 170<br>\n18 880<br>\n8 580<br>\n3 000\n</div>\n\n</td><td>\n\n<div style=\"text-align:center\">\n<b>7 DO</b><br>\n+<br>\n+<br>\n-<br>\n-<br>\n-\n</div>\n\n</td><td>\n\n<div style=\"text-align:center\">\n<b>Fabrikas</b><br>\n+<br>\n+<br>\n+<br>\n+<br>\n+\n</div>\n\n</td><td>\n\n<div style=\"text-align:right\">\n<b>Enerģija kopā</b><br>\n44 460<br>\n41 840<br>\n37 760<br>\n17 160<br>\n6 000\n</div>\n\n</td></tr></tbody></table><br><i>Atgādinājums visiem - pieteikties var līdz WC rangam, bet sākot ar CMS tiek kompensēti 20hp par katru kilu</i><br><br><b>★ Nedēļas sākumā enerģijas uzkrājums 0 enerģijas.<br>\n★ Kopā iztērēti 33566.72cc pārtikas iegādē.<br>\n★ Kopā šonedēļ izdalīts enerģijas apjoms 147220 enerģijas.<br>\n★ Enerģijas uzkrājums uz nākamo nedēļu - 0 enerģijas.</b><br><br><br><b>MAIZES APGĀDEI UZ NĀKAMO NEDĒĻU PIESAKĀMIES ŠAJĀ RAKSTĀ ZEM KARA MINISTRIJAS KOMENTĀRA, AR NORĀDI - piesakos!.<br>\nJa pieteikumā nebūs norādīts vārds \"piesakos\", tad uz apgādi var netikt pieskaitīts!</b><br><br><img src=\"https://dl.dropboxusercontent.com/s/y30q3d4ymeenzfa/Atdalitajs.png\" class=\"bbcode_img\"><br><br><b>Prasības pārtikas pretendentiem:</b><br><br>\n★ Latvietis sirdī un pēc pases - jābūt mūsu valsts pilsonim.<br><b>★ Aircraft rank līdz Wing Commander (neieskaitot) (līdz 1'673'000 aircraft rank points).</b><br>\n★ Pilotam ir jāpiesakās uz pārtiku KM raksta komentāros, kurā tiek izziņots par maizes apgādi tekošajai nedēļai.<br>\n★ Izdarīto kilu apjomam jābūt apskatāmam nedeļas valsts top 100 statistikā.<br><br>\nPēc pieprasījuma saņemšanas KM komanda izskata pieprasījumu, tiek pārbaudīts nedēļas laikā izdarītais kilu skaits gaisa kaujās. Nedēļas laikā izdarīto kilu skaitu reizinam ar <b>30, ja gaisa rangs līdz Chief Master Sergeant, bet sākot ar Chief Master Sergeant 20</b>, kas arī būs enerģijas apjoms, ko valsts kompensē jaunajam pilotam.<br><br><b>Papildu nosacījumi un pateicības atrodami <a href=\"https://www.erepublik.com/en/article/2712063\">šeit</a></b><br><br>\n- KM labprāt sagaida arī pārtikas ziedotājus.<br>\n- Pārtikas ziedotāju saraksts, pārtikas izlietojums tiks publicēts KM avīzē, rakstā, kurā piesakās pārtikai.<br><br><img src=\"https://dl.dropboxusercontent.com/s/y30q3d4ymeenzfa/Atdalitajs.png\" class=\"bbcode_img\"><br><br>\nAtceramies:<br>\nVisi Endorsers aizies pilotu apgādēm.<br><b>Tā kā lasām, ziedojam, atbalstām un karojam!</b><br><br><img src=\"https://dl.dropboxusercontent.com/s/y30q3d4ymeenzfa/Atdalitajs.png\" class=\"bbcode_img\"><br><br>\nAktuālie kauju paziņojumi tiek izziņoti:<br>\n* eLatvijas laika joslā (erepublik)<br>\n* <a href=\"//www.erepublik.com/en/main/warn/aHR0cHM6Ly9kaXNjb3JkYXBwLmNvbS9pbnZpdGUvV3dGNWgyMw==\"><b>eLatvijas Discord serverī</b></a> #valdības_paziņojumi<br><br><img src=\"https://dl.dropboxusercontent.com/s/y30q3d4ymeenzfa/Atdalitajs.png\" class=\"bbcode_img\"><br><br>\nApgādi veica: <b><a href=\"https://www.erepublik.com/en/citizen/profile/1620414\">inpoc1</a></b><br><br><br><div style=\"text-align:center\">\n<a href=\"https://www.erepublik.com/en/newspaper/187543/1\"><img src=\"https://dl.dropboxusercontent.com/s/34u16bcgfdsly2d/EkonomikasMinistrija.jpg\" class=\"bbcode_img\"></a><a href=\"https://www.erepublik.com/en/newspaper/201132\"><img src=\"https://dl.dropboxusercontent.com/s/gr9u0hfmk3j2ykt/KaraMinistrija.jpg\" class=\"bbcode_img\"></a><a href=\"https://www.erepublik.com/en/newspaper/207943\"><img src=\"https://dl.dropboxusercontent.com/s/650f20nxo3fkaxz/LabklajibasMinistrija.jpg\" class=\"bbcode_img\"></a><a href=\"https://www.erepublik.com/en/newspaper/220672\"><img src=\"https://dl.dropboxusercontent.com/s/j7kr1ebcd6fwylu/ValstsKanceleja.jpg\" class=\"bbcode_img\"></a><a href=\"https://www.erepublik.com/en/newspaper/235010\"><img src=\"https://dl.dropboxusercontent.com/s/1cjdt91ytnbplri/ArlietuMinistrija.jpg\" class=\"bbcode_img\"></a><a href=\"https://www.erepublik.com/en/newspaper/190402\"><img src=\"https://dl.dropboxusercontent.com/s/41dlgh2j6vv53pd/IzglitibasMinistrija.jpg\" class=\"bbcode_img\"></a>\n</div>"}}""")
