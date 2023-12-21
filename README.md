# MinidimSharp
 MinidimSharp er et værktøj til at dimensionere elektriske installationer med udgangspunkt i DS/HD 60364-serien: "Standardsamling til installationsbekendtgørelsen".
 
 ---------------------------------------------------------------------------
 
![image](https://github.com/GhaithA-M/MinidimSharp/assets/122114790/cb2753aa-910d-4bf3-a107-2b72fbe8246d)

1:	Udregn belastningsstrøm: (Dimensioneringsstrøm)


2:	Vælg OB / KB og fastlæg In


3:	Fastlæg installationsmetode


4:	Fastlæg temperatur: Temperaturkoffiecent


5	Fastlæg om samlet fremføring


6:	Udregn nødvendig kontinuerlig strømværdi for kablet


7:	Bestem belastningsgrad


8:	Kontrol af betingelse 1


9:	Evt. Kontrol af KB og spændingsfald


 ---------------------------------------------------------------------------


Trin 1: Design af brugergrænseflade


    Design en formular med inputfelter for hver variabel, du har brug for at indsamle.

    Formularen skal give brugerne mulighed for at indtaste værdier for belastningsstrøm, installationsmetode, omgivelsestemperatur, kabelgruppe (samlet fremføring), kablets kontinuerlige strømstyrke (Kx) osv.


Trin 2: Indsamling af input


    Indsaml input til:

        Beregning af belastningsstrøm (Dimensioneringsstrøm)

        Afbrydertype (OB / KB) og mærke (IN (SM) eller (AS)) eller indstilling af IR (MA)

        Installationsmetode

        Temperaturkoefficient baseret på omgivende forhold

        Kabelgrupperingsfaktor (Sf)


Trin 3: Beregninger


    Gennemfør beregningerne som defineret i IEC 60364-standarden. Dette vil sandsynligvis involvere:

        Beregning af kablets kontinuerlige strømstyrke (Kx) baseret på input og referencediagrammer.

        Beregning af derating-faktorer for temperatur, kabelgruppering, installationsmetode osv.

        Verificering af, at den beregnede strøm ikke overstiger kablets kapacitet, justeret for nedreguleringsfaktorer (kt, ks, kx osv.).


Trin 4: Validering


    Tilføj kontroller for at validere input i henhold til standardens krav.

    Implementer tilstandskontrollen: IB=INIB?=IN? og IR=Iz-kt-ks-kx-etc.IR?=Iz?-kt?-ks?-kx?-etc.

    Trin 5: Output


    Vis resultaterne for brugeren, herunder den anbefalede kabelstørrelse og eventuelle advarsler, hvis betingelserne ikke er opfyldt.

    Inkluder eventuelt muligheden for at kontrollere spændingsfald (KB og spændingsfald) i henhold til standarden.


Trin 6: Referencer til standarddiagrammer


    Du bliver nødt til at digitalisere diagrammerne fra IEC 60364-standarden, så din applikation kan referere til dem i beregningerne.

    Dette kan gøres ved at konvertere diagrammerne til et digitalt format som CSV eller direkte implementering i en database.


Trin 7: Brugervejledning og dokumentation


    Lav en brugervejledning, der forklarer hvert trin, og hvordan man fortolker resultaterne.

    Dokumenter beregningsmetoderne og henvis til de specifikke afsnit i IEC 60364-standarden, der gælder.


Trin 8: Test og validering


    Test applikationen grundigt med forskellige scenarier for at sikre nøjagtighed.

    Det kan være nødvendigt at få applikationens beregninger valideret af en certificeret elektroingeniør eller en person med ekspertise i IEC 60364-standarden.


Trin 9: Kontrol af overholdelse


    Sørg for, at din applikation overholder standarden og eventuelle juridiske krav til software, der leverer tekniske beregninger.

Trin 10: Iteration og brugerfeedback


    Efter den indledende udvikling skal du indsamle feedback fra potentielle brugere.

    Finpuds applikationen baseret på denne feedback og eventuelle ændringer i de relevante standarder.


Til den egentlige kodning skal du oversætte disse trin til det programmeringssprog, du vælger, designe en brugergrænseflade, skrive funktioner til beregningerne og håndtere brugerinput/output.

Hvis du kan oplyse, hvilket programmeringssprog eller framework du bruger, kan jeg give dig mere detaljeret vejledning om kodestrukturen og de biblioteker, der kan være nyttige til dette projekt.