import { Formik, Form, Field, ErrorMessage } from 'formik';
import css from './ContactForm.module.css'
import { nanoid } from 'nanoid'
import * as Yup from "yup";
import { useDispatch } from 'react-redux';
import { addContact } from '../../redux/contactsSlice' 


export default function ContactForm() {
    const dispatch = useDispatch();

    const ContactSchema = Yup.object().shape({
      name: Yup.string()
        .min(3, "Too Short!")
        .max(50, "Too Long!")
        .required("Name is required"),
      phone: Yup.string()
        .matches(/^\+?[1-9][0-9-\s]{6,14}$/, "Invalid phone number format")
        .required("Phone number is required"),
    });
  
    const handleSubmit = (values, actions) => {

      const newContact ={
        id: nanoid(),
        name: values.name,
        number: values.phone,
      }
      console.log('New contact:', newContact);
      dispatch(addContact(newContact)); // Додаємо контакт через dispatch
      actions.resetForm();
    };
  
    const nameFieldId = nanoid();
    const phoneFieldId = nanoid();
  
    return (
        <Formik
          initialValues={{ name: '', phone: '' }}
          onSubmit={handleSubmit}
          validationSchema={ContactSchema}
        >
          <Form className={css.form}>
            <label htmlFor={nameFieldId} className={css.label}>
            Name
            </label>
            <Field
              id={nameFieldId}
              name="name"
              type="text"
              className={css.field}
            />
            <ErrorMessage name="name" component="span" className={css.error} />
    
            <label htmlFor={phoneFieldId} className={css.label}>
            Phone
            </label>
            <Field
              id={phoneFieldId}
              name="phone"
              type="tel"
              className={css.field}
            />
            <ErrorMessage name="phone" component="span" className={css.error} />
    
            <button className={css.btn} type="submit">
              Submit
            </button>
          </Form>
        </Formik>
      );
    }