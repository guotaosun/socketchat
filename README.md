# TCP-Chat Pythonilla
### <i> "bestest chaet serviec"
> <b> Tietokoneverkot projekti

>Tuomas Takko 427612

>Jesse Merilampi

## Yleiskuvaus
> Projektin tavoitteena on toteuttaa useamman kuin kahden samanaikaisen käyttäjän keskusteluohjelma käyttäen pythonia. Toteutus tehdään ensin ilman graafista ulkoasua, jonka jälkeen muodostetaan yksinkertainen käyttöliittymä pyQt4:lla.

## Vaatimukset
- Useampi kuin 2 samanaikaista käyttäjää
- Backlog serverillä
- Käyttäjätunnus (nickname)
- Turvallisuus/Toimintavarmuus
- Useampi huone?

## Suunnitelma/Dokumentaatio
#### Rakenne
> Kevyt UML-kaavio/muu abstrakti kuvaustapa.
#### Funktiot
Client:
- main (perustoiminallisuus)
- prompt (chatin toiminnallisuus tulostukseen)

Server:
- main (perustoiminnallisuus)
- broadcast_data (viestin jakaminen)

Database:
- backlogi

GUI:
- window


## TODO

- Tiedostot+tietokanta
- Client
- Server
- Dokumentaatio
- Testaus
- GUI
