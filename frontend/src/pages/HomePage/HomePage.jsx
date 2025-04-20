// import ContactForm from '../../components/ContactForm/ContactForm';
// import SearchBox from '../../components/SearchBox/SearchBox';
// import ContactList from '../../components/ContactList/ContactList';

// const HomePage = () => {
//   return (
//     <>
//       <ContactForm />
//       <SearchBox />
//       <ContactList />
//     </>
//   );
// };

// export default HomePage;

import { Link } from 'react-router-dom';
import css from './HomePage.module.css';

export default function HomePage() {
  return (
    <section className={css.homePage}>
      <div className='container'>
        <h1 className={css.title}>Contacts — closer <br />than they appear</h1>
        <h2 className={css.titleInfo}>Easy. Fast. Green</h2>
        <Link className={css.viewBtn} to='/auth/register'>Register Now</Link>
      </div>
    </section>
  );
}