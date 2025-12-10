# Lielo valodas modeļu izmantošana CQL vaicājumu ģenerēšanai marķētos teksta korpusos
(CQL - Corpus Query Language)

## Plāns

### 1. Izveidot testu kopu
Jāizveido testu kopu ar kuru varētu novērtēt modeļu spēju ģenerēt CQL vaicājumus.
Testu kopai nepieciešams > ~1000 testu gadījumu.

#### 1.1. Uzģenerēt CQL vaicājumus ar vaicājumu aprakstiem
Ar uzģenerētajiem vaicājumiem varēs iegūt no korpusiem sagaidāmo rezultātu katram aprakstam.

#### 1.2. Apvienot CQL vaicājumus ar vaicājumu rezultātiem no korpusa
Lai novērtētu modeļus ir nepieciešams sagaidāms kāds ir sagaidāmais rezultāts CQL pieprasījumiem.
Jāiegūst no viena izvēlēta korpusa (es izvēlējos korpusu "LVK2022") un jāsaglabā pieprasījumu rezultātus. Korpusa.lv nosketch engine CQL pieprasījumi atgriež rezultātā atgriež vairākas kolonas par dokumentu, kurā atrasts pieprasījumam atbilstošā konkordance. 

Svarīgākais no visiem - KWIC (Key Word In Context), kas tiks izmantots kā sagaidāmais rezultāts modeļu ģenerētajiem CQL pieprasījumiem.

### 2. Izveidot skriptu modeļu novērtēšanai	
Skripts, kas