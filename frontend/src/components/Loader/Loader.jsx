import {  FaPlane } from 'react-icons/fa'; 
import { ClipLoader } from 'react-spinners';
import css from './Loader.module.css'

const Loader = () => {
  return (
    <div className={css.loaderContainer}>
      <div className={css.travelLoader}>
        <ClipLoader size={50} color="#ff6347" />
        <FaPlane size={60} color="#ff6347" />
      </div>
      <span>Loading travel adventures...</span>
    </div>
  );
};

export default Loader;