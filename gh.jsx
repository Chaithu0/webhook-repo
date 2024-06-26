import React, { useState, useEffect } from 'react';
import axios from 'axios';
const App = () => {
const [events, setEvents] = useState([]);
useEffect(() => {
const fetchEvents = async () => {
try {
const response = await axios.get('http://localhost:3000/events');
setEvents(response.data);
} catch (error) {
console.error('Error fetching events:', error);
}
};
fetchEvents();
const interval = setInterval(fetchEvents, 15000);
return () => clearInterval(interval);
}, []);
return (
<div>
<h1>GitHub Events</h1>
<ul>
{events.map((event, index) => (
<li key={index}>
{event.event_type === 'push' && (
<div>
{event.author} pushed to {event.to_branch} on{' '}
{new Date(event.timestamp).toLocaleString()}
</div>
)}
{event.event_type === 'pull_request' && (
<div>
{event.author} submitted a pull request from {event.from_branch}
to{' '}
{event.to_branch} on {new Date(event.timestamp).toLocaleString()}
</div>
)}
{event.event_type === 'merge' && (
<div>
{event.author} merged branch {event.from_branch} to
{event.to_branch} on{' '}
{new Date(event.timestamp).toLocaleString()}
</div>
)}
</li>
))}
</ul>
</div>
);
};
export default App;