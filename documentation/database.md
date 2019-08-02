

Kantakuvaus:
------------

Kokoelma:
* artisti:Artist
* artistin_alias:Alias
* nimi:String
* tiedoston_nimi:String
* Kokoelma:Blob
* ryhma:Ryhma
* julkaisuvuosi:int
* lisaaja:Kayttaja
* lisatty:DateTime
* julkinen:Boolean

Artisti:
 * nimi:String
 * ensisijainen_ryhma:Ryhma
 * lisattu:DateTime
 * ryhmat:Ryhma*
 * alias:Alias*
 * kokoelmat:Kokoelma*

Ryhma:
 * nimi:String
 * jasenet:Artisti*

Kayttaja:
 * luotu:DateTime
 * tunnus:String
 * sahkoposti:String
 * salasana-hash:String
 * oikeustaso:int

Jasenyys:
 * ryhma:Ryhma
 * artisti:Artisti

Alias:
 * alias:String
 * Artisti

Viesti:
 * lahettaja:Kayttaja
 * vastaanottaja:Kayttaja
 * paivamaara:DateTime
 * luettu:Boolean
 * lahettajan_poistama:Boolean
 * vastaanottajana_poistama:Boolean

Piste:
 * pisteyttaja:Kayttaja
 * kokoelma:Kokoelma
 * pisteet:int
 * annettu:DateTime

Kommentti:
 * kommentoija:Kayttaja
 * kommentti:String
 * luotu:DateTime

Kaavio [yuml.me](http://yuml.me) lähdekoodina:
----------------------------
```
[Kokoelma|artisti:Artisti;artistin_alias:String;nimi:String;kokoelman_nimi:String;tiedoston_nimi:String;sisalto:Blob;julkaisuryhma:Ryhma;julkaisuvuosi:int;lisatty:DateTime;julkinen:Boolean]

[Artisti|nimi:String;aliakset:Alias*;kokoelmat:Kokoelma*;ensisijainen_ryhma:Ryhma;ryhmat:Ryhma;lisatty:DateTime]

[Jasenyys|ryhma:Ryhma;artisti:Artisti]

[Viesti|lahettaja:Kayttaja;vastaanottaja:Kayttaja;paivamaara:DateTime;luettu:Boolean;lahettajan_poistama:Boolean;vastaanottajan_poistama:Boolean]

[Kayttaja|tunnus:String;sahkoposti:String;luotu:DateTime;sahkoposti:String;salasana:String;oikeustaso:int]

[Alias|alias:string;artisti:Artisti]

[Kommentti|kommentoija:Kayttaja;kommentti:String;luotu:DateTime]

[Piste|pisteyttaja:Kayttaja;kokoelma:Kokoelma;pisteet:int;annettu:DateTime]

[Artisti]1-1..*[Alias]
[Kokoelma]1-1>[Artisti]
[Kokoelma]*-1>[Kayttaja]
[Kokoelma]1-*>[Piste]
[Kokoelma]1-*>[Kommentti]
[Artisti]++-0..*>[Jasenyys]
[Viesti]2-0..*[Kayttaja]

```

