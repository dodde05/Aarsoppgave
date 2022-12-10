# Veiledning for videre utvikling

## Prosjektets innhold

- game (mappe)
- website (mappe)
- serversetup.sh

Mappen 'game' innholder all kode til selve spillet.  
Mappen 'website' inneholder all kode til spillets nettside, og hører til serverside.

## Oppsett

### Webserver

Innholdet i 'website' hostes med en webserver. Husk å sette webserverens filprioritet til php ovenfor html.  

### Database

For å kjøre hele oppsettet på egenhånd, må det også opprettes en database. Både MySQL og MariaDB kan benyttes.  
Websiden og spillet er fra før av programmert til å koble seg på en database med følgende oppsett:
Database med navn 'highscores' med 1 tabell, 'attempts'. Tabellen har 4 kolonner: 'id', 'name', 'score', 'date'. Kolonnene har henholdsvis følgende datatyper: INT, VARCHAR(15), DECIMAL(6, 2), DATE. I tillegg må det være en bruker på databasen med navn 'client' og passord '79E76w864dcKbja'. Brukeren må minst ha lese- og skriverettigheter.
Ønskes det å bruke et annet databaseoppsett, må det endres på i koden. game/game.py og website/index.php er de eneste filene som kobler seg til database.