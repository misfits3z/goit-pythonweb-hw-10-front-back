import { useDispatch, useSelector } from 'react-redux';
import { selectNameFilter, changeFilter } from '../../redux/filtersSlice';
import css from './SearchBox.module.css';

export default function SearchBox() {
  const dispatch = useDispatch();
  const filter = useSelector(selectNameFilter); //Підписка на стан фільтра

  const handleChange = (e) => {
    dispatch(changeFilter(e.target.value));
  };

  return (
    <div className={css.search}>
      <label htmlFor="search">Find contacts by name</label>
      <input
        id="search"
        type="text"
        value={filter}
        onChange={handleChange}
        placeholder="Search..."
      />
    </div>
  );
}

// export default function SearchBox ({value, onChange}){
//   return(
//   <div className={css.search}>
//     <label htmlFor="search">Find contacts by name</label>
//     <input 
//       type="text" 
//       value={value}
//       onChange={onChange}
//       placeholder="Search..."
//       />
//   </div>
//   )
// }