import {
  Container,
  IngredientsSearch,
  FileInput,
  Input,
  Title,
  CheckboxGroup,
  Main,
  Form,
  Button,
  Textarea,
} from "../../components";
import styles from "./styles.module.css";
import api from "../../api";
import { useEffect, useState } from "react";
import { useTags } from "../../utils";
import { useHistory } from "react-router-dom";
import MetaTags from "react-meta-tags";
import { Icons } from "../../components";
import cn from "classnames";

const RecipeCreate = ({ onEdit }) => {
  const { value, handleChange, setValue } = useTags();
  const [recipeName, setRecipeName] = useState("");
  const history = useHistory();
  const [ingredientValue, setIngredientValue] = useState({
    name: "",
    id: null,
    amount: "",
    measurement_unit: "",
  });
  const [recipeIngredients, setRecipeIngredients] = useState([]);
  const [recipeText, setRecipeText] = useState("");
  const [recipeTime, setRecipeTime] = useState("");
  const [recipeFile, setRecipeFile] = useState(null);

  const [ingredients, setIngredients] = useState([]);
  const [showIngredients, setShowIngredients] = useState(false);
  const [submitError, setSubmitError] = useState({ submitError: "" });
  const [ingredientError, setIngredientError] = useState("");

  const handleAddIngredient = () => {
    if (
      ingredientValue.amount !== "" &&
      !/^\d+$/.test(ingredientValue.amount)
    ) {
      return setIngredientError("Количество ингредиента должно быть целым числом");
    }

    if (
      ingredientValue.amount === "" ||
      ingredientValue.name === "" ||
      !ingredientValue.id
    ) {
      return setIngredientError("Ингредиент не выбран");
    }

    if (recipeIngredients.find(({ name }) => name === ingredientValue.name)) {
      return setIngredientError("Ингредиент уже выбран");
    }

    setRecipeIngredients([...recipeIngredients, ingredientValue]);
    setIngredientValue({
      name: "",
      id: null,
      amount: "",
      measurement_unit: "",
    });
  };

  useEffect(
    (_) => {
      if (ingredientValue.name === "") {
        return setIngredients([]);
      }
      api.getIngredients({ name: ingredientValue.name }).then((ingredients) => {
        setIngredients(ingredients);
      });
    },
    [ingredientValue.name]
  );

  useEffect((_) => {
    api.getTags().then((tags) => {
      setValue(tags.map((tag) => ({ ...tag, value: true })));
    });
  }, []);

  const handleIngredientAutofill = ({ id, name, measurement_unit }) => {
    setIngredientValue({
      ...ingredientValue,
      id,
      name,
      measurement_unit,
    });
  };

  const checkIfDisabled = () => {
    if (
      recipeText === "" ||
      recipeName === "" ||
      recipeIngredients.length === 0 ||
      recipeTime === "" ||
      recipeFile === "" ||
      recipeFile === null
    ) {
      setSubmitError({ submitError: "Заполните все поля!" });
      return true;
    }

    if (value.filter((item) => item.value).length === 0) {
      setSubmitError({ submitError: "Выберите хотя бы один тег" });
      return true;
    }
    return false;
  };

  return (
    <Main>
      <Container>
        <MetaTags>
          <title>Создание рецепта</title>
          <meta name="description" content="Фудграм - Создание рецепта" />
          <meta property="og:title" content="Создание рецепта" />
        </MetaTags>
        <Title title="Создание рецепта" />
        <Form
          className={styles.form}
          onSubmit={(e) => {
            e.preventDefault();
            if (checkIfDisabled()) {
              return;
            }
            const data = {
              text: recipeText,
              name: recipeName,
              ingredients: recipeIngredients.map((item) => ({
                id: item.id,
                amount: item.amount,
              })),
              tags: value.filter((item) => item.value).map((item) => item.id),
              cooking_time: recipeTime,
              image: recipeFile,
            };
            api
              .createRecipe(data)
              .then((res) => {
                history.push(`/recipes/${res.id}`);
              })
              .catch((err) => {
                const { non_field_errors, ingredients, cooking_time } = err;
                if (non_field_errors) {
                  return setSubmitError({
                    submitError: non_field_errors.join(", "),
                  });
                }
                if (ingredients) {
                  return setSubmitError({
                    submitError: `Ингредиенты: ${
                      ingredients
                        .filter((item) => Object.keys(item).length)
                        .map((item) => {
                          const error = item[Object.keys(item)[0]];
                          return error && error.join(" ,");
                        })[0]
                    }`,
                  });
                }
                if (cooking_time) {
                  return setSubmitError({
                    submitError: `Время готовки: ${cooking_time[0]}`,
                  });
                }
                const errors = Object.values(err);
                if (errors) {
                  setSubmitError({ submitError: errors.join(", ") });
                }
              });
          }}
        >
          <Input
            label="Название рецепта"
            onChange={(e) => {
              setSubmitError({ submitError: "" });
              setIngredientError("");
              const value = e.target.value;
              setRecipeName(value);
            }}
            className={styles.mb36}
          />
          <CheckboxGroup
            label="Теги"
            values={value}
            emptyText="Нет загруженных тегов"
            className={styles.checkboxGroup}
            labelClassName={styles.checkboxGroupLabel}
            tagsClassName={styles.checkboxGroupTags}
            checkboxClassName={styles.checkboxGroupItem}
            handleChange={handleChange}
          />
          <div className={styles.ingredients}>
            <div className={styles.ingredientsInputs}>
              <Input
                label="Ингредиенты"
                className={styles.ingredientsNameInput}
                inputClassName={styles.ingredientsInput}
                placeholder="Начните вводить название"
                labelClassName={styles.ingredientsLabel}
                onChange={(e) => {
                  setSubmitError({ submitError: "" });
                  setIngredientError("");
                  const value = e.target.value;
                  setIngredientValue({
                    ...ingredientValue,
                    name: value,
                  });
                }}
                onFocus={(_) => {
                  setShowIngredients(true);
                }}
                value={ingredientValue.name}
              />
              <div className={styles.ingredientsAmountInputContainer}>
                <p className={styles.amountText}>в количестве </p>
                <Input
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      handleAddIngredient();
                    }
                  }}
                  className={styles.ingredientsAmountInput}
                  inputClassName={styles.ingredientsAmountValue}
                  onChange={(e) => {
                    setSubmitError({ submitError: "" });
                    setIngredientError("");
                    const value = e.target.value;
                    setIngredientValue({
                      ...ingredientValue,
                      amount: value,
                    });
                  }}
                  placeholder={0}
                  value={ingredientValue.amount}
                  type="number"
                />
                {ingredientValue.measurement_unit !== "" && (
                  <div className={styles.measurementUnit}>
                    {ingredientValue.measurement_unit}
                  </div>
                )}
              </div>
              {showIngredients && ingredients.length > 0 && (
                <IngredientsSearch
                  ingredients={ingredients}
                  onClick={({ id, name, measurement_unit }) => {
                    handleIngredientAutofill({ id, name, measurement_unit });
                    setIngredients([]);
                    setShowIngredients(false);
                  }}
                />
              )}
            </div>
            <div className={styles.ingredientAdd} onClick={handleAddIngredient}>
              Добавить ингредиент
            </div>
            {ingredientError && (
              <p className={cn(styles.error, styles.errorIngredient)}>
                {ingredientError}
              </p>
            )}
            <div className={styles.ingredientsAdded}>
              {recipeIngredients.map((item) => {
                return (
                  <div className={styles.ingredientsAddedItem}>
                    <span className={styles.ingredientsAddedItemTitle}>
                      {item.name}
                    </span>
                    <span>, </span>{" "}
                    <span>
                      {item.amount}
                      {item.measurement_unit}
                    </span>{" "}
                    <span
                      className={styles.ingredientsAddedItemRemove}
                      onClick={(_) => {
                        const recipeIngredientsUpdated =
                          recipeIngredients.filter((ingredient) => {
                            return ingredient.id !== item.id;
                          });
                        setRecipeIngredients(recipeIngredientsUpdated);
                      }}
                    >
                      <Icons.IngredientDelete />
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
          <div className={styles.cookingTime}>
            <Input
              label="Время приготовления"
              className={styles.ingredientsTimeInput}
              labelClassName={styles.cookingTimeLabel}
              inputClassName={styles.ingredientsTimeValue}
              onChange={(e) => {
                const value = e.target.value;
                setRecipeTime(value);
              }}
              value={recipeTime}
              placeholder="0"
            />
            <div className={styles.cookingTimeUnit}>мин.</div>
          </div>
          <Textarea
            label="Описание рецепта"
            onChange={(e) => {
              const value = e.target.value;
              setRecipeText(value);
            }}
            placeholder="Опишите действия"
          />
          <FileInput
            onChange={(file) => {
              setRecipeFile(file);
            }}
            fileTypes={["image/png", "image/jpeg"]}
            fileSize={5000}
            className={styles.fileInput}
            label="Загрузить фото"
          />
          <Button modifier="style_dark" type="submit" className={styles.button}>
            Создать рецепт
          </Button>
          {submitError.submitError && (
            <p className={styles.error}>{submitError.submitError}</p>
          )}
        </Form>
      </Container>
    </Main>
  );
};

export default RecipeCreate;
