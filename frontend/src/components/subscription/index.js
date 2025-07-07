import styles from "./styles.module.css";
import { useState } from "react";
import { Button, LinkComponent, Popup } from "../index";
import DefaultImage from "../../images/userpic-icon.jpg";

const countForm = (number, titles) => {
  number = Math.abs(number);
  if (Number.isInteger(number)) {
    let cases = [2, 0, 1, 1, 1, 2];
    return titles[
      number % 100 > 4 && number % 100 < 20
        ? 2
        : cases[number % 10 < 5 ? number % 10 : 5]
    ];
  }
  return titles[1];
};

const Subscription = ({
  email,
  first_name,
  last_name,
  username,
  removeSubscription,
  recipes_count,
  id,
  recipes,
  avatar,
}) => {
  const shouldShowButton = recipes_count > 3;
  const moreRecipes = recipes_count - 3;
  const [toDelete, setToDelete] = useState(false);

  return (
    <div className={styles.subscription}>
      {toDelete && (
        <Popup
          title="Вы уверены, что хотите отписаться?"
          onSubmit={() => {
            removeSubscription({
              id,
              callback: () => {
                setToDelete(false);
              },
            });
          }}
          onClose={() => {
            setToDelete(false);
          }}
        />
      )}
      <div className={styles.subscriptionHeader}>
        <h2 className={styles.subscriptionTitle}>
          <div
            className={styles.subscriptionAvatar}
            style={{
              "background-image": `url(${avatar || DefaultImage})`,
            }}
          />
          <LinkComponent
            className={styles.subscriptionRecipeLink}
            href={`/user/${id}`}
            title={`${first_name} ${last_name}`}
          />
        </h2>
      </div>
      <div className={styles.subscriptionBody}>
        <ul className={styles.subscriptionItems}>
          {recipes.map((recipe) => {
            return (
              <li className={styles.subscriptionItem} key={recipe.id}>
                <LinkComponent
                  className={styles.subscriptionRecipeLink}
                  href={`/recipes/${recipe.id}`}
                  title={
                    <div className={styles.subscriptionRecipe}>
                      <img
                        src={recipe.image}
                        alt={recipe.name}
                        className={styles.subscriptionRecipeImage}
                      />
                      <h3 className={styles.subscriptionRecipeTitle}>
                        {recipe.name}
                      </h3>
                      <p className={styles.subscriptionRecipeText}>
                        {recipe.cooking_time} мин.
                      </p>
                    </div>
                  }
                />
              </li>
            );
          })}
          {shouldShowButton && (
            <li className={styles.subscriptionMore}>
              <LinkComponent
                className={styles.subscriptionLink}
                title={`Еще ${moreRecipes} ${countForm(moreRecipes, [
                  "рецепт",
                  "рецепта",
                  "рецептов",
                ])}...`}
                href={`/user/${id}`}
              />
            </li>
          )}
        </ul>
      </div>
      <div className={styles.subscriptionFooter}>
        <Button
          className={styles.subscriptionButton}
          clickHandler={(_) => {
            setToDelete(true);
          }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="20"
            viewBox="0 0 16 20"
            fill="none"
          >
            <path
              d="M14 10H2"
              stroke="black"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          Отписаться
        </Button>
      </div>
    </div>
  );
};

export default Subscription;
