import Header from "../Header/Header";
import { Link } from "react-router-dom";
import css from './AppBar.module.css'
// import logoTravel from '../../images/logoTravel.svg'



export default function AppBar() {
  return (
      <header className={css.header}>
          <div className={css.headerContent}>
            <Link className={css.logo} to="/">     
              {/* <img src={logoTravel} width="136" height="15" /> */}
            </Link>
                <Header />
          </div>
    </header>
  );
}