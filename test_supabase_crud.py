# test_supabase_crud.py
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """
    Punto de entrada para la ejecución de la prueba.
    """
    load_dotenv()
    
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_SERVICE_KEY"):
        logging.error("❌ Faltan las variables de entorno SUPABASE_URL o SUPABASE_SERVICE_KEY.")
        return

    logging.info("✅ Variables de entorno cargadas.")

    from src.core.services.supabase_test_service import SupabaseTestService

    test_service = SupabaseTestService()
    test_service.run_test()

if __name__ == "__main__":
    main()