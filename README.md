# Meitar_app
Pet project: creating a repertoire search app for my choir, and evolving it into an insights app.

This project was born out of a desire to use the tools I learned on my path toward a new career direction to simplify my life in my current workplace.

Since 2014, I have worked as assistant conductor at the "Meitar" children's choir in the Rehovot Conservatory — the same choir I grew up in as a child and where I had my first experience as a singer and musician.
The choir's library and catalog that we inherited from the founder conductor of the choir, Mrs. Yehudit Chen (Z"L), was a printed copy of a file on her computer (that is no longer available to us) with some handwritten additions. Already at the time we inherited it, it was outdated and missing newer entries. This made recording the new pieces we added to the repertoire even more messy and inconsistent. Being able to manage, add, and search for the piece_ID (and therefore the location of the music sheets in the physical library) would be much easier with an app.
Another problem this app is intended to solve for us is facilitating the search of pieces in the choir's repertoire (by title, composer, language, and so on).

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Table Schemas:

Repertoire:
|Field |	Type |	Notes |
| :------: | :------: | ------| 
| repertoire_category	| text	| Category indicator (see key) |
| serial_number	| integer	| The order number within the category |
| title	| text	| Name of the piece |
| composer |	text |	Cannot be null. Use “Anonymous” if unknown. |
| arranger	| text (nullable) |	Null allowed if there is no arrangement |
| lyrics	| text	| poet or text origin. Cannot be null. Use “Anonymous” if unknown. |
| translator	| text	(nullable) |	Null allowed if there is no translation |
| language	| text | Composed/lyrics language |
| voicing	| text	| SATB / SSA / SA + optional comments |
| with_boys	| boolean	| Whether boys (male voices) participate |
| accompanied	| boolean	| Whether there is instrumental accompaniment |
| instruments	| text | Free-text list of instruments (“piano, violin, darbuka…”) |
| music_present	| boolean	| Whether the choir owns printed music materials |

Performance:
| Field	| Type	| Notes |
|:----------:| :--------: | ----- |
| date	| date	| Performance date |
| occasion	| text	| name of the event |
| piece_title	| text	| name of a piece song |
| piece_serial	| UID | (foreign key to Repertoire)	Repertoire.category + serial_number |
| order_in_program	| integer	| the sequence of the pieces as performed |
| estimated_time	| timestamp | duration of the piece in seconds or minutes | 
