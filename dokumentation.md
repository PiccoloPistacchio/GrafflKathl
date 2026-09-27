Logbuch – GrafflKathl

Sprint 1: 21.08. bis 27.08.2026

Sprintziel: Eine lauffähige Webanwendung aufbauen, in der sich Nutzer registrieren, anmelden und ihr Profil aufrufen können. Damit steht die Grundlage für die weiteren Funktionen.

21.08.2026 – Projektstart und Einrichtung
Heute ging es erst einmal darum, das Projekt überhaupt zum Laufen zu bringen. Ich habe die Projektstruktur angelegt, eine virtuelle Python-Umgebung eingerichtet und Flask installiert. Das hat länger gedauert als gedacht, vor allem weil die PowerShell zwischendurch nicht so wollte wie ich. Am Ende ließ sich aber eine erste Seite im Browser öffnen. Noch nicht besonders aufregend, aber immerhin: GrafflKathl lebt.

23.08.2026 – Datenbank und Registrierung
SQLite wurde eingebunden und mit SQLAlchemy ein erstes Modell für die Benutzer erstellt. Danach kam das Registrierungsformular dazu. Beim Test wurde tatsächlich ein Benutzer in der Datenbank gespeichert.
Dann habe ich gemerkt, dass Passwörter nicht im Klartext dort stehen sollten. Deshalb habe ich die Speicherung anschließend auf Passwort-Hashes umgestellt. 

25.08.2026 – Login und Benutzerprofil
Auf der Registrierung konnte ich den Login aufbauen. Richtige Zugangsdaten führen zur Anmeldung, ein falsches Passwort wird abgelehnt. Damit angemeldete Nutzer beim Seitenwechsel erkannt werden, habe ich außerdem die Session-Verwaltung ergänzt.
Nach der Anmeldung gelangt man zum eigenen Profil. Dort werden zunächst Name und E-Mail-Adresse angezeigt. Eine Logout-Funktion wurde auch hinzugefügt.

27.08.2026 – Test und Sprint Review
Zum Abschluss habe ich Registrierung, Login, Profil und Logout mit zwei Testnutzern durchgespielt. Die Abläufe funktionieren. Zwischendurch gab es vor allem Probleme mit Einrückungen, Imports und einzelnen Routen. Bei Python reicht offenbar schon eine Zeile am falschen Platz, um mir den Nachmittag zu beschäftigen.

Retrospektive: Für den nächsten Sprint möchte ich Änderungen in kleineren Schritten einbauen und direkt testen. Der Zeitplan war für meinen Kenntnisstand ziemlich sportlich. Allerdings stresst es mich tatsächlich eine feste Frist zu haben. Damit muss ich noch lernen umzugehen. Fokus auf die gesetzten Prioritäten zu halten, fällt mich aber schwer. Andererseits habe ich gemerkt, dass ich mehr Grundlagen mitbringe als gedacht und gezielter nach Lösungen suchen kann, sobald ich das Problem eingegrenzt habe. Ein kleines Schulterklopfen ist also drin. 

Sprint 2: 28.08. bis 03.09.2026
Sprintziel: Nutzer sollen eigene Gegenstände einstellen und verwalten können. Andere Nutzer sollen verfügbare Gegenstände reservieren und eine Reservierung wieder aufheben können.

28.08.2026 – Gegenstände anlegen
Ich habe das Datenmodell um ein paar Gegenstände erweitert. Jeder Gegenstand hat unter anderem einen Namen, eine Beschreibung, einen Verfügbarkeitsstatus und einen Besitzer. Über ein Formular können angemeldete Nutzer nun eigene Gegenstände einstellen.
Der erste Testgegenstand ließ sich speichern und wurde dem richtigen Benutzer zugeordnet. Aus der Benutzerverwaltung wird langsam eine Verleihplattform.

30.08.2026 – Übersicht, Bearbeiten und Löschen
Die eingestellten Gegenstände erscheinen jetzt in einer gemeinsamen Übersicht. Danach habe ich Funktionen zum Bearbeiten und Löschen ergänzt. Dabei musste ich darauf achten, dass nur der Besitzer seinen Gegenstand verändern kann. Mit eigenen und fremden Testgegenständen habe ich beide Fälle geprüft. Die Perspektive des jeweiligen Nutzers zu beachten hat mich ein paar mal durcheinander gebracht. Es hat geholfen mir das einmal auf einem Schmierpapier aufzumalen, wer was sehen soll. 

01.09.2026 – Reservierungen
Nun kam die Reservierungsfunktion dazu. Ein verfügbarer Gegenstand kann von einem anderen Nutzer reserviert werden. Nach der Reservierung ändert sich der Verfügbarkeitsstatus automatisch.
Für den Test habe ich zwischen zwei Benutzerkonten gewechselt. So konnte ich prüfen, ob der Gegenstand aus Sicht der ausleihenden Person reservierbar ist und danach nicht noch einmal angeboten wird. Mein Learning daraus? Mir zu merken, welches Passwort ich für die Testnutzer verwende und auch wie meine Testnutzer heißen.

03.09.2026 – Eigene Reservierungen und Sprint Review
Nutzer können ihre Reservierungen jetzt in einer eigenen Übersicht sehen und wieder aufheben. In diesem Fall wird der Gegenstand erneut freigegeben. Ich habe den Ablauf vom Einstellen über das Reservieren bis zum Aufheben einmal vollständig getestet.
Zwischendurch hatte ich beim Ergänzen neuer Funktionen Codeblöcke ungünstig platziert.  Dadurch funktionierte vorübergehend sogar die Registrierung aus Sprint 1 nicht mehr. Das hat mich heute an die Grenzen meiner Stressresistenz gebracht. Nachdem ich die Struktur der app.py bereinigt hatte, lief alles wieder.

Retrospektive: Das direkte Testen nach einzelnen Änderungen hat sich bewährt. Außerdem komme ich derzeit besser zurecht, wenn ich einen zusammenhängenden Codeblock in Ruhe fertigstelle, statt an mehreren Stellen gleichzeitig kleine Änderungen vorzunehmen. Ich verliere zu schnell den Überblick und lasse mich zu schnell ablenken. Die Anwendung besteht inzwischen aus mehr als einzelnen Testseiten. Kathl weiß jetzt zumindest schon, wer welches Graffl haben möchte.

Sprint 3: 04.09. bis 10.09.2026
Sprintziel: Aus einer Reservierung soll eine Ausleihe werden. Besitzer und ausleihende Person sollen Übergabe und Rückgabe jeweils selbst bestätigen können.

04.09.2026 – Reservierungsanfragen und Ausleihen
Ich habe eine Übersicht für eingegangene Reservierungsanfragen ergänzt. Besitzer sehen damit, wenn jemand einen ihrer Gegenstände reserviert hat. Anschließend habe ich das Datenmodell für Ausleihen angelegt. Darin werden der Gegenstand, beide beteiligten Nutzer und die Bestätigungen für Übergabe und Rückgabe gespeichert.

06.09.2026 – Start und Bestätigung der Übergabe
Eine Reservierung kann nun angenommen und in eine Ausleihe überführt werden. Danach können Besitzer und ausleihende Person die Übergabe unabhängig voneinander bestätigen. Der jeweilige Stand wird bei der laufenden Ausleihe angezeigt.
Das habe ich mit zwei Testkonten geprüft: Erst hat eine Seite bestätigt, dann nach dem Benutzerwechsel die andere. So ließ sich auch sehen, ob eine noch ausstehende Bestätigung korrekt angezeigt wird. Diesesmal hatte ich eine Liste mit den Testkonten unden zugehörigen Passwörtern. 

08.09.2026 – Rückgabe
Für die Rückgabe habe ich denselben Grundgedanken umgesetzt. Sie kann erst bestätigt werden, wenn die Übergabe von beiden Seiten bestätigt wurde. Erst nach beiden Rückgabebestätigungen wird der Gegenstand wieder verfügbar. Die abgeschlossene Ausleihe verschwindet aus der Übersicht der laufenden Ausleihen.

10.09.2026 – Gesamtablauf und Sprint Review
Ich habe den Weg von der Reservierung über die Übergabe bis zur Rückgabe mit zwei Nutzern durchgespielt. Der Kernprozess funktioniert nun vollständig.
Ganz ohne Umwege ging es allerdings nicht: Durch Änderungen am Datenmodell passte die vorhandene SQLite-Datenbank zeitweise nicht mehr zum Code. Da darin nur Testdaten lagen, konnte ich sie neu erstellen. Außerdem hatte ich versehentlich eine Route doppelt angelegt und musste den Code noch einmal durchgehen.

Retrospektive: Bei Änderungen am Datenmodell muss ich genauer hinschauen. db.create_all() passt vorhandene Tabellen nicht einfach an neue Modellfelder an. Für diesen Prototyp war das Zurücksetzen der Testdatenbank eine praktikable Lösung; bei einer Weiterentwicklung bräuchte es dafür Migrationen. Meine Testnutzer waren besonders hilfreich, weil ich den Ablauf wirklich aus mehreren Perspektiven prüfen konnte. 

Sprint 4: 11.09. bis 17.09.2026
Sprintziel: Die vorhandenen Funktionen sollen verständlich erreichbar sein und als zusammenhängende Anwendung funktionieren. Zum Schluss wird der gesamte Ablauf noch einmal getestet.

11.09.2026 – Navigation
Die Funktionen waren inzwischen vorhanden, aber nicht alle Seiten waren bequem erreichbar. Teilweise musste ich noch die passende URL kennen. Deshalb habe ich das Benutzerprofil zu einer zentralen Übersicht erweitert. Von dort aus gelangt man unter anderem zu den Gegenständen, eigenen Reservierungen, eingegangenen Anfragen und laufenden Ausleihen.

13.09.2026 – Anzeigen und Aktionen überarbeiten
In der Gegenstandsübersicht habe ich angepasst, welche Schaltflächen für wen sichtbar sind. Besitzer können ihre Gegenstände bearbeiten oder löschen. Bei fremden verfügbaren Gegenständen wird stattdessen die Reservierung angeboten.
Auch die Anzeigen für die laufenden Ausleihen habe ich noch einmal überprüft. Wenn jemand Übergabe oder Rückgabe bereits bestätigt hat, soll die gleiche Aktion nicht erneut angeboten werden. Die Rückgabe erscheint erst, wenn beide Seiten die Übergabe bestätigt haben. Die Regeln waren damit auch in der Oberfläche besser nachvollziehbar.

15.09.2026 – Gestaltung und Weiterleitungen
Ich habe eine zentrale CSS-Datei eingebunden und die Seiten einheitlicher gestaltet. Es ging mir dabei weniger um ein aufwendiges Design als darum, dass Formulare, Schaltflächen und Übersichten ordentlich lesbar sind.
Einige Weiterleitungen habe ich ebenfalls angepasst: Nach der Registrierung gelangt man zur Anmeldung, nach dem Einstellen eines Gegenstands zur Gegenstandsübersicht. So sieht man direkt, was die eigene Aktion bewirkt hat.

17.09.2026 – Abschließender Test und Sprint Review
Zum Schluss habe ich die Anwendung mit unterschiedlichen Nutzern einmal von Anfang bis Ende durchgespielt: registrieren, anmelden, Gegenstand einstellen, reservieren, Anfrage bearbeiten, Übergabe von beiden Seiten bestätigen, Rückgabe von beiden Seiten bestätigen und den Gegenstand wieder freigeben.
Zusätzlich habe ich geprüft, dass man eigene Gegenstände nicht reservieren und fremde Gegenstände nicht bearbeiten oder löschen kann. Der vollständige Ablauf funktionierte im abschließenden Test.

Retrospektive: Dieser Sprint war ruhiger als die vorherigen, weil keine große neue Fachfunktion mehr dazukam. Dafür wurde deutlich, wie wichtig die Benutzerführung ist. Eine Funktion hilft wenig, wenn man erst ihre URL kennen muss, um sie zu finden. Rückblickend hätte ich die Navigation früher mitdenken können. Für den Prototyp sind die Funktionen jetzt aber zu einem nachvollziehbaren Ablauf zusammengewachsen. 

Erster Eindruck für mein Fazit: 
Mit einem Zeitplan zu arbeiten ist eine Herausforderung. Vor allem zu Beginn eines Sprints hatte ich immer das Bedürfnis so viel wie möglich zu schaffen. Nur um dann das Testen zu vernachlässigen und eine aufwändigere Fehlersuche betreiben zu müssen. Daran muss ich noch arbeiten. 
Die Zusammenarbeit mit meinen Nachbarn wiederum war super. Sehr lieb, dass sie mir ihre Zeit gegeben haben, um mir zu helfen. Es ist auch spannend mit jemanden zu reden, der nicht in der Thematik drin ist und ihm das so zu erklären, dass man alle abholen kann. Daraus folgt nochmal ein ganz anderes eigenes Grundverständnis. 
Also, alles in allem viel hausgemachter Stress, der sich vermeiden lassen würde, wenn ich meinem eigenen Zeitplan mehr vertraut hätte. 