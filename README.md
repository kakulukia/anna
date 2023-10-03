# anna

Zum Installieren von Modulen 'poetry install' nutzen.
Zum Hinzufügen von neuen Modulen 'poetry add xy' nutzen.

master: gl = git pull, zieht Neuerungen im aktuellen Branch auf den Rechner.
branch mika: Hier geht nur git merge master!

# Zulip Profilfelder
'full_name': 'Andy Grabow',
'delivery_email': 'andy@freilandkiwis.de',
'realm_id': 2
'default_language': 'de',
'twenty_four_hour_time': True,
'color_scheme': 2

# Service neustart
pm2 list > zeigt alle laufenden Services an
pm2 restart anna > startet den Service neu
pm2 logs anna > zeigt die letzten Logs (und folgende an)

# install pre-commit hooks
pre-commit install


# Close Webhook updaten
 HTTPie App hat die entsprechenden Anfragen bereits gespeichert:
1. Lokalen Server starten und mit ngrok von extern erreichbar machen.
2. Via update Webhook die URL ändern, sodass Anfragen jetzt bei mir landen
3. Wenn alles fertig ist: Updates bei live einspielen und Webhook wieder zurück ändern
