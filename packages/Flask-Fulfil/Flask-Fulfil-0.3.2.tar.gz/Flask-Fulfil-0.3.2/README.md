# Flask-Fulfil

Flask-Fulfil is a Flask extension that provides Fulfil.IO API client for
your application.

Whether you are building an e-commerce store or a simple dashboard using
Fulfil.IO data, this plugin is handy to use Fulfil with your app.

## Installation

Install the extension with one of the following commands:

    $ easy_install flask-fulfil

of alternatively if you have pip installed:
    
    $ pip install flask-fulfil

## Usage

To use the extension simply import the class wrapper and pass the Flask app
object back to here. Do so like this:
    
    from flask import Flask
    from flask.ext.fulfil import Fulfil
    
    app = Flask(__name__)
    fulfil = Fulfil(app)

The primary method exposed is to pull up resources also called models. For
example, to pull up the product model::

    Product = fulfil.model('product.product')
    iphones = Product.search(['name', 'ilike', 'iphone'])
