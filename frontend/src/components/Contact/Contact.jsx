import { FaUser, FaPhone} from 'react-icons/fa'
import css from './Contact.module.css'
import { useDispatch } from 'react-redux';
import { deleteContact } from '../../redux/contactsSlice'
// import ContactList from '../ContactList/ContactList';

export default function Contact({ id, name, number }) {

    const dispatch = useDispatch()

    const handleDelete = () => {
        dispatch(deleteContact(id));
      };



    return (
        <div className={css.contact}>
        <li className={css.card}>
            <p><FaUser className={css.icon}/>{name}</p>
            <p><FaPhone className={css.icon}/>{number}</p>
        </li>
        <button onClick={() => handleDelete(id)}>Delete</button>
    </div>
    );
}