import { useEffect } from 'react';
import SearchBox from './components/SearchBox/SearchBox';
import ContactList from './components/ContactList/ContactList';
import ContactForm from './components/ContactForm/ContactForm';
import './App.css';
import { useDispatch } from 'react-redux';
import { selectContacts } from './redux/contactsSlice';
// import { addContact, deleteContact } from './redux/contactSlice'; 
// import { changeFilter } from './redux/filtersSlice'; 

function App() {
  const dispatch = useDispatch();

  // Завантаження контактів із localStorage
  useEffect(() => {
    const savedContacts = localStorage.getItem('contacts');
    if (savedContacts) {
      dispatch(selectContacts(JSON.parse(savedContacts)));
    }
  }, [dispatch]);

  return (
    <div>
      <h1>Phonebook</h1>
      <ContactForm />
      <SearchBox />
      <ContactList />
    </div>
  );
}

export default App;

// function App() {
//   const contacts = useSelector((state) => state.contacts.items); // Список контактів
//   const nameFilter = useSelector((state) => state.filters.name); // Фільтр
//   const dispatch = useDispatch();

//   useEffect(() => {
//     const savedContacts = localStorage.getItem('contacts');
//     if (savedContacts) {
//       dispatch(selectContacts(JSON.parse(savedContacts)));
//     }
//   }, [dispatch]);

//   const handleAddContact = (newContact) => {
//     dispatch(addContact(newContact)); // Додаємо контакт через Redux
//   };

//   const handleDeleteContact = (id) => {
//     dispatch(deleteContact(id)); // Видаляємо контакт через Redux
//   };

//   const handleFilterChange = (evt) => {
//     dispatch(changeFilter(evt.target.value))
//   };

//   const filteredContacts = contacts.filter((contact) =>
//     contact.name.toLowerCase().includes(nameFilter.toLowerCase()) 
//   );

//   return (
//     <div>
//       <h1>Phonebook</h1>
//       <ContactForm />
//       <SearchBox/> 
//       <ContactList />
//     </div>
//   );
// }

// export default App;


