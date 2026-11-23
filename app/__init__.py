import os
from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "gelistirme-anahtari")

    from app.moduller.hasta_muayene import hasta_muayene_bp
    from app.moduller.doktor_recete import doktor_recete_bp
    from app.moduller.eczane_satis import eczane_satis_bp
    from app.moduller.ilac_tedarik import ilac_tedarik_bp

    app.register_blueprint(hasta_muayene_bp)
    app.register_blueprint(doktor_recete_bp)
    app.register_blueprint(eczane_satis_bp)
    app.register_blueprint(ilac_tedarik_bp)

    @app.get("/")
    def ana_sayfa():
        return render_template("index.html")

    return app