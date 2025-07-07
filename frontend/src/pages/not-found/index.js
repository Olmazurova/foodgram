import { Button, Container, Main } from "../../components";
import styles from "./styles.module.css";
import image from "../../images/not-found.png";
import { useHistory } from "react-router-dom";

const Favorites = () => {
  const history = useHistory();

  const handleClick = () => history.replace("/recipes");

  return (
    <Main className={styles.root}>
      <Container>
        <img src={image} className={styles.img} alt="логотип." />
        <p className={styles.text}>Страница не найдена</p>
        <Button
          modifier="style_dark"
          className={styles.button}
          onClick={handleClick}
        >
          На главную
        </Button>
      </Container>
    </Main>
  );
};

export default Favorites;
