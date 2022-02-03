import dotenv
import os

def is_it_me(ctx):
    owner = 624076054969188363
    
    return ctx.author.id == int(owner)