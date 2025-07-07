import {
  Container,
  Input,
  FormTitle,
  Main,
  Form,
  Button,
} from "../../components";
import styles from "./styles.module.css";
import { useFormWithValidation } from "../../utils";
import { AuthContext } from "../../contexts";
import { Redirect } from "react-router-dom";
import { useContext } from "react";
import MetaTags from "react-meta-tags";
import { ChangePasswordText } from "../../components/change-password-text";

const ChangePassword = ({ onPasswordChange, submitError, setSubmitError }) => {
  const { values, handleChange, errors, isValid, resetForm } =
    useFormWithValidation();
  const authContext = useContext(AuthContext);

  const onChange = (e) => {
    setSubmitError({ submitError: "" });
    handleChange(e);
  };

  return (
    <Main withBG asFlex>
      <Container className={styles.center}>
        <MetaTags>
          <title>Изменить пароль</title>
          <meta
            name="description"
            content="Фудграм - Изменить пароль"
          />
          <meta property="og:title" content="Изменить пароль" />
        </MetaTags>
        <Form
          className={styles.form}
          onSubmit={(e) => {
            e.preventDefault();
            onPasswordChange(values);
          }}
        >
          <FormTitle>Изменить пароль</FormTitle>
          <Input
            required
            isAuth={true}
            placeholder="Старый пароль"
            type="password"
            name="current_password"
            error={errors}
            onChange={onChange}
          />
          <Input
            required
            isAuth={true}
            placeholder="Новый пароль"
            type="password"
            name="new_password"
            error={errors}
            onChange={onChange}
          />
          <ul className={styles.texts}>
            <li className={styles.text}>
              <ChangePasswordText text="Ваш пароль не должен совпадать с вашим именем или другой персональной информацией или быть слишком похожим на неё" />
            </li>
            <li className={styles.text}>
              <ChangePasswordText text="Ваш пароль должен содержать как минимум 8 символов" />
            </li>
            <li className={styles.text}>
              <ChangePasswordText text="Ваш пароль не может быть одним из широко распространённых паролей" />
            </li>
            <li className={styles.text}>
              <ChangePasswordText text="Ваш пароль не может состоять только из цифр" />
            </li>
          </ul>
          <Input
            required
            isAuth={true}
            placeholder="Подтвердите новый пароль"
            type="password"
            name="repeat_password"
            error={errors}
            submitError={submitError}
            onChange={onChange}
          />
          <Button
            modifier="style_dark"
            type="submit"
            className={styles.button}
            disabled={
              !isValid || values.new_password !== values.repeat_password
            }
          >
            Изменить пароль
          </Button>
        </Form>
      </Container>
    </Main>
  );
};

export default ChangePassword;
