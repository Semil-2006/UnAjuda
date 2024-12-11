from flask import Flask, render_template, request, redirect, url_for, session
from banco_dados_logi import Usuario, Session
from oauthlib.oauth2 import WebApplicationClient 
import requests

