ASCII-kokoelmien arkisto
=========================
80-luvulta lähtien on Amigalla tehty ja julkaistu ASCII-logokokoelmia BBS-maailmaan liittyvillä sisällöillä.
Kokoelmia on julkaistu tuhansia ja niitä ovat julkaisseet eri artistit eri ryhmien alaisuudessa sekä itsenäisesti.

Sama artisti voi esiintyä usealla eri pseudonyymillä ja eri ryhmillä. Kuka tahansa käyttäjä voi selata kokoelmia lisäyspäivämäärän, artistin, ryhmän käyttäjien antaman pisteytyksen mukaan. Rekisteröityneet käyttäjät voivat lisätä niitä. Sekä rekisteröinnin yhteydessä että kokoelman lisäyksen yhteydessä on moderointi / aktivointi.
Arkisto sisältää sosiaalisia ominaisuuksia kuten yksityisviestit sekä pasteboardin missä käyttäjä voi kevyesti jakaa tekeleitään.


Toimintoja:
-----------
* Rekisteröityminen (Aktivointi)
* Sisäänkirjautuminen
* Kokoelmien listaus
* Kokoelman katselu
* Kokoelman lisäys
* Kokoelman katselmus (moderointi)
* Kokoelman kommentointi ja arvostelu
* Pasteboard
* Yksityisviesti


Kantakuvaus:
------------

Yksinkertainen kuvaus kannasta sekä yuml.me-palveluun sopiva lähdekoodi sille

Kokoelma:
* artisti:artist
* artistin_alias:Alias
* nimi
* tiedoston_nimi:String
* Kokoelma:Blob
* ryhma:Ryhma
* julkaisuVuosi:int
* lisaaja:Kayttaja
* lisatty:DateTime
* julkinen:Boolean

Artisti:
 * nimi:String
 * alias:Alias*
 * kokoelmat:Kokoelma*
 * ensisijainen_ryhma:Ryhma
 * ryhmat:Ryhma*
 * lisattu:DateTime

Ryhma:
 * nimi:String
 * jasenet:Artisti*

Kayttaja:
 * luotu:DateTime
 * tunnus:String
 * sahkoposti:String
 * salasana-hash:String
 * oikeustaso:int

Jasenyydet:
 * ryhma:Ryhma
 * artisti:Artisti

Aliakset:
 * Artisti
 * Alias

Viestit:
 * lahettaja:Kayttaja
 * vastaanottaja:Kayttaja
 * paivamaara:DateTime
 * luettu:Boolean
 * lahettajan_poistama:Boolean
 * vastaanottajana_poistama:Boolean


Kaavio yuml.me lähdekoodina:

[Kokoelma|artisti:Artisti;artistin_alias:String;nimi:String;kokoelman_nimi:String;tiedoston_nimi:String;sisalto:Blob;julkaisuryhma:Ryhma;julkaisuvuosi:int;lisatty:DateTime;julkinen:Boolean]

[Artisti|nimi:String;aliakset:Alias*;kokoelmat:Kokoelma*;ensisijainen_ryhma:Ryhma;ryhmat:Ryhma;lisatty:DateTime]

[Jasenyydet|ryhma:Ryhma;artisti:Artisti]

[Viesti|lahettaja:Kayttaja;vastaanottaja:Kayttaja;paivamaara:DateTime;luettu:Boolean;lahettajan_poistama:Boolean;vastaanottajan_poistama:Boolean]

[Kayttaja|tunnus:String;sahkoposti:String;luotu:DateTime;sahkoposti:String;salasana:String;oikeustaso:int]


[Alias|alias:string;artisti:Artisti]

[Artisti]1-1..*[Alias]
[Kokoelma]1-1>[Artisti]
[Kokoelma]*-1>[Kayttaja]


[Artisti]++-0..*>[Jasenyydet]

[Viesti]2-0..*[Kayttaja]


