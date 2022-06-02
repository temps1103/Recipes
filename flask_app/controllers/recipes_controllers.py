from dataclasses import dataclass
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User




@app.route("/new/recipe")
def new_recipe():
    return render_template("new_recipe.html")


@app.route("/create/recipe", methods=["post"])
def create_recipe():
    if 'user_id' not in session:
        flash("Please log in to see this page")
        return redirect('/')

    under_30_yes = request.form.get("under_30_yes")
    under_30 = False
    if under_30_yes == 'on':
        under_30 = True


    query_data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "date_made" : request.form["date_made"],
        "under_30" : under_30,
        "user_id" : request.form["user_id"]
    }
   
    Recipe.create_new_recipe(query_data)
    return redirect("/dashboard")




@app.route("/one_recipe/<int:recipe_id>")
def one_recipe(recipe_id):
    query_data = {
        "id" : recipe_id        
    }
    
    user = User.get_by_id({ "id": session['user_id']} )
    one_recipe = Recipe.get_one_recipe(query_data)
    return render_template("one_recipe.html", one_recipe = one_recipe, user = user)


@app.route("/delete_recipe/<int:user_id>")
def delete_recipe(user_id):
    query_data = {
        "id" : user_id
    }
    Recipe.delete_recipe(query_data)
    return redirect("/dashboard")


@app.route("/update_recipe/<int:id>")
def edit_recipe(id):
    data = {'id': id}
    recipe = Recipe.get_one_recipe(data)    
    return render_template("edit_recipe.html",recipe=recipe)


@app.route("/edit_recipe/<int:id>", methods=["post"])
def update_recipe(id):

    under_30_yes = request.form.get("under_30_yes")
    under_30 = False
    if under_30_yes == 'on':
        under_30 = True

    query_data = {
        'id': request.form["id"],
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "under_30" : under_30
    }

    Recipe.update_recipe(query_data)
    return redirect("/dashboard") 