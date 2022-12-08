# Prosjektbeskrivelse
Et grafisk plattformspill der poeng kan lastes opp til en database og vises på en nettside.

## Client side
### Spillet
Spillet er programmert i python, stort sett med pygame-biblioteket. Målet er å løpe rundt og hoppe for å unngå kanonkulene som skytes inn fra sidene. Poeng avgjøres ut ifra hvor lenge man overlever.

## Server side
Serveren hostes på en dedikert maskin med Linux.

### Databasen
MariaDB brukes som database. Databasen inneholder 1 tabell, som videre inneholder 4 kolonner: id, navn, poeng og dato.

### Webserveren
Apache brukes som webserver. Nettsidens forside viser poengtavla til spillet, hentet direkte fra databasen med php, og en knapp til en annen side. Den skal inneholde link til å laste ned spillet.
