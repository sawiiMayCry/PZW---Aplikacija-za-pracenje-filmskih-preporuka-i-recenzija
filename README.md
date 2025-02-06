//sara ivankovic
Aplikacija za praćenje filmskih preporuka i recenzija

Aplikacija omogućava pregled filmova i recenzija te unos, ažuriranje i brisanje istih.

Stvoreni modeli za 
filmove (Movies), 
recenzije (Reviews), 
"lajkovi" od strane korisnika (User movies),
preporuke za filmove od strane korisnika (Movie recommendations),
preporuke za filmove (User recommendations).

Baza podataka popunjena testnim podacima koristeći factory_boy.


Projektni zadatak 1

korisnici stvoreni koristeći factory_boy su preimenovani i postavljene su im nove lozinke

ADMIN
ivsar
123

korisnik1            
5678dcba 

korisnik2
5678dcba

korisnik3            
5678dcba

korisnik4
5678dcba 

korisnik5           
5678dcba             


Za navedene korisnike omogućena je prijava i odjava.

08.12.

Omogućena prijava administratora sa početne stranice

Sada se prilikom prijave ispisuje popis filmova, popis preporučenih filmova i popis "lajkanih" filmova.
Na toj stranici se nalazi link za preporuke odnosno ostatak modela baze.


15.12.

dodani listView, DetailView, pretraživanje filmova (po naslovu) i recenzija (po korisniku)

dodano još testnih podataka, u admin sučelju promjenjeni passwordi i imena usera - korisnik6, korisnik7, korisnik8. Lozinke odgovaraju onima drugih korisnika.

omogućeno "lajkanje" filmova ulogiranim korisnicima.

21.12.

C - dodavanje recenzija i preporuka putem forme postoji od prije

R - pretraživanju filmova dodano filtriranje

U - napravljeno ažuriranje recenzija i preporuka koje je napisao korisnik.

D - Dodano brisanje recenzija i preporuka koje je korisnik stvorio.

20.1.

omogućen REST API za GET, POST, GET po ID-u i DELETE po ID-u za ulogiranog korisnika nad modelom Review odnosno nad recenzijama.

omogućen dohvat svih instanci modela Movie

GET /api/reviews/

POST /api/reviews/

GET /api/reviews/id/

PUT /api/reviews/id/

DELETE /api/reviews/id/


GET /api/movies


31.1.

napravljeno testiranje modela, url-ova i pogleda.

python .\manage.py test .\main\tests\


05.02.

napravljen dizajn koristeći 6 css datoteka