# OpenStreetMap data wrangling, SQL design and data analysis

This project uses data munging techniques, such as assessing the quality of the data for validity, accuracy, completeness, consistency and uniformity to clean data on the maps of Dublin available on OpenStreetMap. After auditing and cleaning the dataset it is converted from XML to CSV format and imported into a SQL database. 

## Data overview
The full XML file was parsed and the number of top level tags were quantified in order to get an overall view of the data.

Types and quantities of nodes:
 `'bounds': 1`
 `'member': 91716`
 `'nd': 2028541`
 `'node': 1469711`
 `'relation': 4989`
 `'tag': 1060747`
 `'way': 269763`

Below is a summary of string structures of the key (“k”) descriptions in the “tag” nodes.

   |       |All “k” descriptions|
   |-------|:------------------:|
   |lower  |673577|
   |lower\_colon|342839|
   |problemchars|0|
   |other|44331|

## Problems identified
Through programmatic auditing, the following problems were identified:

*Completeness issues*
* Missing user ID and user name in a “nodes” node: one node did not have any entry for user – neither user name, nor ID.
* Often phone numbers were filled in with underscores as the contributor likely didn't have the correct information to fill in that particular field when entering data on a place.

*Consistency issues*
* The programmatic audit of street names helped me identify a number of issues with the consistency of street name representation. Some of the problems were due to the use of different types of abbreviations, use or non-use of the dot ‘.’ character, etc. In other cases, inconsistency arose due to use of two different languages – English and Irish, both of which are prevalent in identifying areas in Dublin.  Overall, I identified 5 types of required corrections to street names, which I included in the “mapping” dictionary, which served as an input for the “update_name” function, which I subsequently incorporated in the “shape_element” function.
* Phone numbers were in a major disarray, presented in lots of different and sometimes hard to comprehend formats. A standard representation of landline phone numbers in Dublin follows the format of +353-01-XXX-XXXX. Mobile numbers follow the same standard but the three-digit code after the country code (+38) varies by operator. In addition, there are some local 800 numbers, which usually follow the format 08X-XXX-XXXX. 
* Post codes (which are more commonly known as Eircodes in Ireland) were largely inconsistent as Ireland only recently started using the. Before postcodes were introduced in Ireland there were area codes within Dublin which would take the format "Dublin 2" or "D2" which would specify a partivular region of Dublin. However, the new Eircodes identified specific buildings and take the form of XXX-XXXX. Unsuprisingly, the maps of Dublin used both the old format of postcodes as well as the new Eircodes. For each of the old post codes there are now hundreds of unique Eircodes in it's place so it was not possible to programmatically replace the old postcodes. However, the Eircodes that were used were arranged into the same formatin order to make it easier for querying the database later.

## Data exploration through SQL database

### Users(contributors)
Counting unique users in both “nodes” and “ways” nodes and ranking them by the number of appearance:

`sqlite> SELECT t.user, COUNT(*) as num
        FROM (
            SELECT user FROM nodes UNION ALL SELECT user FROM ways
            ) t
        GROUP BY t.user
        ORDER BY num DESC
        LIMIT 5;`
        
### Amenities
I retrieved all unique types of amenities by the following query:

`sqlite> SELECT value, COUNT(*) AS num
        FROM nodes_tags
        WHERE nodes_tags.key = 'amenity'
        GROUP BY value
        ORDER BY num DESC 
        LIMIT 10; `
        
### Religion:
Ireland is a religious country with a largely Christian population so it'll be interesting to see the ratio of different religions within Dublin.

`sqlite> SELECT nodes_tags.value, COUNT(*) as num
        FROM nodes_tags 
            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') t
            ON nodes_tags.id=t.id
        WHERE nodes_tags.key='religion'
        GROUP BY nodes_tags.value
        ORDER BY num DESC;`
        
## Additional ideas
Suggestions for improving the data accuracy in OpenStreetMap include:

* Make all letters in postcodes uppercase - If OSM stored all letters in postcodes in uppercase there would be a bit more consistency.
* There should be documentation on standard practices, e.g. for phone numbers whether to use brackets, dashes and spaces. Some fields had underscores filled in as the user who entered the data probably didn't know that bit of information. There could also check to make sure that just numbers have been entered, no special characters, except + which is often used in area codes.
* Additionally OSM could have guidelines for whether addresses contain full names or abbreviated name for example, "Avenue" or "Ave."
