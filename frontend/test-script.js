const testScript = `
INT. CAFE - DAY

Sarah sits at a window table, nursing a coffee. Through the window, we see the busy city street. John enters, looking nervous.

JOHN
(checking his watch)
Sorry I'm late.

SARAH
You're always late.

John sits. A waitress approaches.

WAITRESS
Can I get you anything?

JOHN
Just coffee, black.

The waitress leaves. Sarah and John sit in awkward silence.

SARAH
So, why did you want to meet?

JOHN
(beat)
I'm leaving town. Tonight.

Sarah stares at him, shocked.

EXT. CITY STREET - NIGHT

John walks alone, carrying a duffel bag. Sarah runs after him.

SARAH
You can't just leave like this!

JOHN
I have to. They're coming.

A black SUV turns the corner, headlights blazing.

INT. ABANDONED WAREHOUSE - NIGHT

John and Sarah burst through the door, breathing heavily. The warehouse is vast, filled with old machinery.

SARAH
Who are they?

JOHN
The less you know, the safer you are.

Footsteps echo outside. John pulls Sarah behind a large crate.
`;

fetch('http://localhost:3001/api/generate-schedule', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ scriptText: testScript })
})
.then(response => response.json())
.then(data => console.log(JSON.stringify(data, null, 2)))
.catch(error => console.error('Error:', error));