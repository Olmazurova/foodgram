import styles from "./style.module.css";
import { Tooltip } from "react-tooltip";
import { LinkComponent, Icons, Button, TagsContainer, Popup } from "../index";
import { AuthContext } from "../../contexts";
import { useContext, useState } from "react";
import cn from "classnames";
import DefaultImage from "../../images/userpic-icon.jpg";

const Card = ({
  name = "Без названия",
  id,
  image,
  is_favorited,
  is_in_shopping_cart,
  tags,
  cooking_time,
  author = {},
  handleLike,
  handleAddToCart,
  updateOrders,
}) => {
  const authContext = useContext(AuthContext);
  const [toLogin, setToLogin] = useState(false);
  const [whiteSpaceValue, setWhiteSpaceValue] = useState("nowrap");

  return (
    <div className={styles.card}>
      {toLogin && (
        <Popup
          title={
            <>
              <LinkComponent href="/signin" title="Войдите" /> или{" "}
              <LinkComponent href="/signup" title="зарегистрируйтесь" />, чтобы
              сохранить рецепт
            </>
          }
          onClose={() => {
            setToLogin(false);
          }}
        />
      )}
      <TagsContainer tags={tags} className={styles.card__tag} />

      <LinkComponent
        href={`/recipes/${id}`}
        title={
          <div
            className={styles.card__image}
            style={{ backgroundImage: `url(${image})` }}
          />
        }
      />
      <div className={styles.card__body}>
        <LinkComponent
          className={styles.card__title}
          href={`/recipes/${id}`}
          title={name}
          style={{ whiteSpace: whiteSpaceValue }}
          onMouseEnter={() => {
            setWhiteSpaceValue("normal");
          }}
          onMouseLeave={() => {
            setWhiteSpaceValue("nowrap");
          }}
        />
        <div className={styles.card__data}>
          <div
            className={styles["card__author-image"]}
            style={{
              "background-image": `url(${author.avatar || DefaultImage})`,
            }}
          />
          <div className={styles.card__author}>
            <LinkComponent
              href={`/user/${author.id}`}
              title={`${author.first_name} ${author.last_name}`}
              className={styles.card__link}
            />
          </div>
          <div className={styles.card__time}>{cooking_time} мин.</div>
        </div>
        <div className={styles.card__controls}>
          <Button
            className={styles.card__add}
            clickHandler={(_) => {
              if (!authContext) {
                return setToLogin(true);
              }
              handleAddToCart({
                id,
                toAdd: Number(!is_in_shopping_cart),
                callback: updateOrders,
              });
            }}
          >
            {is_in_shopping_cart ? (
              <>
                <Icons.CheckIcon />
                Рецепт добавлен
              </>
            ) : (
              <>
                <Icons.PlusIcon /> Добавить в покупки
              </>
            )}
          </Button>

          <Button
            modifier="style_none"
            clickHandler={(_) => {
              if (!authContext) {
                return setToLogin(true);
              }
              handleLike({ id, toLike: Number(!is_favorited) });
            }}
            className={cn(styles["card__save-button"], {
              [styles["card__save-button_active"]]: is_favorited,
            })}
            data-tooltip-id={id}
            data-tooltip-content={
              is_favorited ? "Удалить из избранного" : "Добавить в избранное"
            }
            data-tooltip-place="bottom"
          >
            <Icons.LikeIcon />
          </Button>
          <Tooltip id={id.toString()} />
        </div>
      </div>
    </div>
  );
};

export default Card;
