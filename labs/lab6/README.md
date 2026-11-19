# Cloud Lab 6 Submission — API Gateway and DynamoDB

Copy this template to `cc-lab-YOUR_ID/lab6/README.md` in your own repository. Follow [the instructions](lab6-instruction.md). Put your screenshots in `lab6/images/` and your three scripts in `lab6/`.

- **Student name:**
- **Student ID:**
- **Learner Lab user name:**
- **Date completed:**

---

## 1. DynamoDB table

![Fruits table](images/01-dynamodb-table.png)

## 2. Table items

![Items in the Fruits table](images/02-dynamodb-items.png)

## 3. REST API resources

![API resources and methods](images/03-api-resources.png)

## 4. GET mapping template

![GET mapping template](images/04-get-mapping-template.png)

## 5. POST /fruit

![POST request](images/05-post-request.png)

## 6. GET /fruit/{name}

![GET request](images/06-get-request.png)

## 7. Stage and Invoke URL

![Stage v1](images/07-stage.png)

## Scripts

- [populate_table.py](populate_table.py)
- [get_fruit.py](get_fruit.py)
- [add_fruit.py](add_fruit.py)

---

## Questions

1. `Apple / Red` and `Apple / Green` are two separate items. Why does DynamoDB accept two items with the same `Name`?
2. Your API's `GET` method sends a `POST` request to DynamoDB. Explain why.
3. What does a mapping template do? Use your GET template as the example: where does each value come from?
4. What happened when you called `GET /fruit/Apple` **without** the `color` parameter? Why?
5. This API has no server and no Lambda function. Name one advantage and one limit of integrating API Gateway directly with DynamoDB.

## Problems and how I solved them (optional)

## AI note (optional)

One suggestion an AI tool gave you and how you checked it.

## Clean up

- [ ] `FruitsAPI` deleted.
- [ ] `Fruits` table deleted.
