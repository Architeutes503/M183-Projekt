# Users

- root:root -> admin
- test:test -> normal user

# Django

Wir haben Django verwendet, da es ein simple und einfach zu verwendete Bibliothek, welche uns viel unnötige Arbeit erspart. Da wir auch schon  in mehreren früheren Projekten Django verwendet haben, kannten wir uns  schon damit aus und mussten uns nicht mehr einarbeiten. Django hat uns vor allem bei der Benutzerverwaltung geholfen, das uns zum Beispiel schon ein Adminpanel geboten hat. Da wir schon mehrere Projekte mit Django umgesetzt haben, konnten wir auch alte Codestücke welche wir schonmal geschrieben haben wiederverwendet und so hatten wir schnell eine gute Grundlage. 

# Passwörter:

Wie oben beschrieben, verwenden wir Django für unser Projekt. Django ist ein Python-basiertes Web-Framework, welcheswir auch verwendet haben um Passwörter sicher zu speichern. Wie wir dies gemacht haben ist unten beschrieben.

1. **Passwort-Hashing:** Django verwendet einen sicheren Passwort-Hashing-Algorithmus, standardmäßig bcrypt, um die Passwörter zu hashen, bevor sie in der Datenbank gespeichert werden. Hashing ist ein unumkehrbarer Prozess, was bedeutet, dass selbst wenn die Datenbank kompromittiert wird, die Passwörter nicht ohne weiteres wiederhergestellt werden können.
2. **Salt:** Um Passwort-Hashes noch sicherer zu machen, verwendet Django sogenannte "Salts". Ein Salt ist eine zufällige Zeichenfolge, die zu jedem Passwort vor dem Hashing hinzugefügt wird. Dadurch wird verhindert, dass identische Passwörter den gleichen Hash-Wert haben.
3. **Password-Strength-Policies:** Django ermöglicht die Implementierung von Passwortrichtlinien, um sicherzustellen, dass Benutzer starke Passwörter verwenden. Entwickler können die Mindestanforderungen an Passwortlänge, die Verwendung von Groß- und Kleinbuchstaben, Ziffern und Sonderzeichen festlegen.
4. **Session-Based Authentication:** Django bietet eingebaute Funktionen für die Authentifizierung von Benutzern, einschließlich Sessions und Cookies. Benutzer werden nach der Anmeldung anhand von Sitzungen authentifiziert, und Django kümmert sich darum, die Sitzungsinformationen sicher zu verwalten.
5. **Passort-Reset-Funktionalität:** Django bietet eine eingebaute Funktionalität für das Zurücksetzen von Passwörtern. Dies ermöglicht es Benutzern, ihr Passwort zurückzusetzen, falls sie es vergessen haben, und stellt sicher, dass dieser Prozess sicher und benutzerfreundlich ist.



# Cross site Scripting

Django verwendet standardmäßig das Konzept des Autoescapings. Dies bedeutet, dass alle von den Benutzern bereitgestellten Daten, die in HTML-Seiten eingefügt werden, standardmäßig automatisch gefiltert und maskiert werden, um schädlichen JavaScript-Code zu verhindern. Dies geschieht durch das Template-System von Django, das Escape-Funktionen für potenziell gefährliche Zeichen wie `<`, `>`, `&`, usw. verwendet.

Zum Beispiel:

```
html
<!-- Django Template -->
<p>{{ user_input|safe }}</p>
```

Mit der `safe`-Filteroption wird Django angewiesen, den Inhalt als sicher zu betrachten und nicht zu escapen. Dies sollte jedoch mit Vorsicht verwendet werden, um XSS-Angriffe zu vermeiden.

**Django Templatesystem:** Wir haben das Templatesystem von Django verwendet, welches uns ermöglicht, sicher mit Benutzereingaben umzugehen. Das Templatesystem bietet Funktionen und Filter, um Daten automatisch zu escapen und somit XSS-Angriffe zu verhindern.

**HTTP Only Cookies:** Django setzt standardmäßig das `HttpOnly`-Attribut für Cookies. Das bedeutet, dass Cookies über JavaScript nicht ausgelesen werden können, was einen weiteren Schutz gegen XSS-Angriffe bietet.

**Middleware-Schutz:** Django enthält spezielle Middleware-Komponenten wie `django.middleware.security.SecurityMiddleware`, die verschiedene Sicherheitsmaßnahmen implementieren. Diese Middleware kann so konfiguriert werden, dass sie bestimmte HTTP-Header setzt, um XSS-Angriffe zu verhindern.
