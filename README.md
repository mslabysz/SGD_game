# Turowa gra na wzór darkest dungeon

## Cel gry
Celem gry jest pokonanie wszystkich przeciwników (bandytów) sterując rycerzem. Gracz może atakować, używać mikstur leczących oraz musi przetrwać ataki przeciwników. Gra kończy się zwycięstwem po pokonaniu wszystkich bandytów lub porażką po śmierci rycerza.

## Zastosowane technologie
- Python 3
- Pygame

## Napotkane problemy i ich rozwiązania
- **Rozmieszczanie elementów na panelu** – elementy (paski HP, licznik mikstur, przyciski) nachodziły na siebie. Rozwiązaniem było testowanie różnych układów i dostosowywanie współrzędnych.
- **Synchronizacja animacji z logiką gry** – animacje ataku, obrażeń i śmierci nie zawsze były zsynchronizowane z faktycznym zadaniem obrażeń lub zmianą stanu gry. Rozwiązaniem było wprowadzenie systemu cooldownów i blokowanie kolejnych akcji do zakończenia animacji.
- **System tur i kolejkowanie akcji** – po wykonaniu akcji przez gracza lub przeciwnika czasem tura nie przechodziła płynnie do kolejnej postaci, co prowadziło do zacięć lub podwójnych ruchów. Rozwiązaniem było wprowadzenie zmiennej current_fighter, action_cooldown oraz resetowanie ich po każdej pełnej turze, co zapewniło płynność rozgrywki i jasny podział na tury.

## Funkcjonalności z listy
- Obsługa myszki (atak, użycie mikstury, przyciski)
- Obsługa klawiatury (wyciszanie/odciszanie dźwięku pod klawiszem "m")
- System pasków energii (HP)
- Przeciwnicy z prostym AI
- Animacje ruchu postaci (atak, otrzymanie obrażeń, śmierć)
- Ulepszenia/bronie/power-upy (mikstury leczące)
- Interfejs użytkownika (UI): dolny panel, licznik mikstur, paski życia, przyciski
- Muzyka w tle
- Efekty dźwiękowe (atak, śmierć, mikstura)
- Możliwość włączenia/wyłączenia dźwięku
- Ekran wygranej i przegranej
- Możliwość restartu gry

## Funkcjonalności spoza listy
- Dynamiczne wyświetlanie obrażeń (DamageText)
- Prosty system tury (kolejność ruchów gracza i przeciwników)



https://github.com/user-attachments/assets/534e0bd5-c75a-4da7-b497-d448fefd8604



---
