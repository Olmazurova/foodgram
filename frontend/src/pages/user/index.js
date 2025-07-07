import {
  Card,
  Title,
  Pagination,
  CardList,
  Button,
  CheckboxGroup,
  Container,
  Main,
  Icons,
} from "../../components";
import cn from "classnames";
import styles from "./styles.module.css";
import { useRecipes } from "../../utils/index.js";
import { useEffect, useState, useContext } from "react";
import api from "../../api";
import { useParams, useHistory } from "react-router-dom";
import { AuthContext, UserContext } from "../../contexts";
import MetaTags from "react-meta-tags";
import DefaultImage from "../../images/userpic-icon.jpg";

const UserPage = ({ updateOrders }) => {
  const {
    recipes,
    setRecipes,
    recipesCount,
    setRecipesCount,
    recipesPage,
    setRecipesPage,
    tagsValue,
    setTagsValue,
    handleTagsChange,
    handleLike,
    handleAddToCart,
  } = useRecipes();
  const { id } = useParams();
  const [user, setUser] = useState(null);
  const [subscribed, setSubscribed] = useState(false);
  const history = useHistory();
  const userContext = useContext(UserContext);
  const authContext = useContext(AuthContext);

  const getRecipes = ({ page = 1, tags }) => {
    api.getRecipes({ page, author: id, tags }).then((res) => {
      const { results, count } = res;
      setRecipes(results);
      setRecipesCount(count);
    });
  };

  const getUser = () => {
    api
      .getUser({ id })
      .then((res) => {
        setUser(res);
        setSubscribed(res.is_subscribed);
      })
      .catch((err) => {
        history.push("/not-found");
      });
  };

  useEffect(
    (_) => {
      if (!user) {
        return;
      }
      getRecipes({ page: recipesPage, tags: tagsValue, author: user.id });
    },
    [recipesPage, tagsValue, user]
  );

  useEffect((_) => {
    getUser();
  }, []);

  useEffect((_) => {
    api.getTags().then((tags) => {
      setTagsValue(tags.map((tag) => ({ ...tag, value: true })));
    });
  }, []);

  return (
    <Main>
      <Container className={styles.container}>
        <MetaTags>
          <title>
            {user
              ? `${user.first_name} ${user.last_name}`
              : "Страница пользователя"}
          </title>
          <meta
            name="description"
            content={
              user
                ? `Фудграм - ${user.first_name} ${user.last_name}`
                : "Фудграм - Страница пользователя"
            }
          />
          <meta
            property="og:title"
            content={
              user
                ? `${user.first_name} ${user.last_name}`
                : "Страница пользователя"
            }
          />
        </MetaTags>
        <div className={styles.title}>
          <div className={styles.titleTextBox}>
            <div className={styles.user}>
              <div
                className={styles.userAvatar}
                style={{
                  "background-image": `url(${
                    (user && user.avatar) || DefaultImage
                  })`,
                }}
              />
              <Title
                className={cn({
                  [styles.titleText]: true,
                })}
                title={user ? `${user.first_name} ${user.last_name}` : ""}
              />
            </div>

            {(userContext || {}).id !== (user || {}).id && authContext && (
              <Button
                className={cn(styles.buttonSubscribe, {
                  [styles.buttonSubscribeActive]: subscribed,
                })}
                modifier={subscribed ? "style_dark" : "style_light"}
                clickHandler={(_) => {
                  const method = subscribed
                    ? api.deleteSubscriptions.bind(api)
                    : api.subscribe.bind(api);
                  method({
                    author_id: id,
                  }).then((_) => {
                    setSubscribed(!subscribed);
                  });
                }}
              >
                <Icons.AddUser />{" "}
                {subscribed ? "Отписаться от автора" : "Подписаться на автора"}
              </Button>
            )}
          </div>

          <CheckboxGroup
            values={tagsValue}
            handleChange={(value) => {
              setRecipesPage(1);
              handleTagsChange(value);
            }}
          />
        </div>

        {recipes.length > 0 && (
          <CardList>
            {recipes.map((card) => (
              <Card
                {...card}
                key={card.id}
                updateOrders={updateOrders}
                handleLike={handleLike}
                handleAddToCart={handleAddToCart}
              />
            ))}
          </CardList>
        )}
        <Pagination
          count={recipesCount}
          limit={6}
          page={recipesPage}
          onPageChange={(page) => setRecipesPage(page)}
        />
      </Container>
    </Main>
  );
};

export default UserPage;
