# Satellite_modell
# Main Tasks

## Konstruktion Vermögensindex aus 43 DHS Umfragen (2009-2016 23 Länder Afrikas)
- Konvertierung von Beschreibung in Score Werte (z.B. Bodentyp)
- Erstellung von Gewichtungen auf Haushaltslevel basierend auf den ersten Hauptkomponenten
 -Längen- und Breitengrad-Koordinaten aus den Umfragedaten extrahieren (pro Cluster)
  - Cluster: - ländliche Gebiete: ungefähr einem Dorf
            - städtische Gebiete ein Stadtteil
- Entfernen von Clustern mit ungültigen GPS Koordinaten (-> 19.669 Cluster) (Rauschen durch Jittering)

- Validierung des Vermögenindex durch Abgleich mit anderen Varianten

- Hinzuziehen von Volkszählungen (die Fragen zum Vermögen enthalten) (2. Adm. Ebene)
				- LSMS Daten 
					  - Ausschluss von Migrantenhaushalten
- Aggregieren aller Daten auf der 2. Administrativen Ebene
- Ausschluss von Variablen die nicht in LSMS verfügbar sind (Kühlschrank, Motorrad)
- *Starke Korrelation zwischen dem konstruierten Vermögensindex und Konsum auf Dorfebene*


## Satellitenbilder
- Export der Nachtlicht- und Tageslichtsatellitenbilder zentriert auf jeden Cluster-Standort (Landsat-Archive Google Earth Engine)
  - 3-Jahres-Median-Komposita (Tageslichtbilder): 
    - 2009-11, 2012-14 und 2015-17
    - Landsat 5,Landsat 7 und Landsat 8
  
        - *Erfassung klarer Satellitenbilder (keine Wolken o.ä.)*
        - *Keine Verzerrung durch kurzzeitige Schwankungen*
        - *Wohlstand entwickelt sich eher langsam*

  - 3-Jahres-Median-Komposita (Nachtlichtbilder)
		-2009-11 (DMSP27)
		-2012-14,2015-17 (VIIRS28)
- Nearest-Neighbor-Upsampling um den gleichen räumlichen Bereich abzudecken

- Slicing der Bilder auf die Eingabegröße des CNN




