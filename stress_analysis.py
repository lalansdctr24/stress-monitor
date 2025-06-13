import re 

class BrainRegion:
    """Kelas dasar area otak dan aktivasi."""
    
    def __init__(self, name, role, value = 0.0):
        # encapsulation (priavtate attribute)
        self.name = name  
        self.role = role
        self.__activation = value  # nilai 0.0 - 1.0

    def set_activation(self, value: float):
        """Mengatur nilai aktivasi, dengan validasi."""
        if not (0.0 <= value <= 1.0):
            # error jika tidak mengembalikan float antara 0.0 dan 1.0
            raise ValueError("Activation must be between 0.0 and 1.0")
        self.__activation = value

    def get_info(self) -> str:
        """Mendapatkan informasi dasar region otak."""
        return f"{self.name} ({self.role}): {self.__activation:.2f}"

    def get_activation(self) -> float:
        """Mendapatkan nilai aktivasi."""
        return self.__activation

class StressAnalyzer(BrainRegion):
    """Menganalisis apakah subjek menunjukkan tanda stres."""

    def __init__(self, brain_regions: list[BrainRegion]):
        self.brain_regions = brain_regions

    def is_stressed(self):
        """
        Logika deteksi stres diperbarui:
        - Amygdala tinggi (> 0.7)
        - PrefrontalCortex rendah (< 0.4)
        - Hippocampus rendah (< 0.5)
        Stres terdeteksi jika Amygdala tinggi DAN (PrefrontalCortex rendah ATAU Hippocampus rendah).
        """
        # get dipakai agar kalau data salah satu area otak tidak ada di log, program kita tidak crash dan tetap punya nilai default
        activations = {r.name: r.get_activation() for r in self.brain_regions}
        amygdala_activation = activations.get("Amygdala", 0.0)
        prefrontal_activation = activations.get("PrefrontalCortex", 1.0)
        hippocampus_activation = activations.get("Hippocampus", 1.0)
        
        amygdala_active = amygdala_activation > 0.7 
        cognitive_memory_dysfunction = prefrontal_activation < 0.4 or hippocampus_activation < 0.5
        
        return amygdala_active and cognitive_memory_dysfunction

    def get_report(self) -> str:
        """Mendapatkan laporan status deteksi stres."""
        status = "STRESSED" if self.is_stressed() else "NORMAL"
        return f"Status Deteksi Stres: {status}"

def parse_brain_log(log_text: str) -> list[tuple[str, str, float]]:
    """
    Ekstrak data aktivasi dari teks log menggunakan Regular Expression.
    Format yang diharapkan: Region=<name>; Role=<role>; Activation=<float>
    """
    # Setiap bagian dalam kurung () adalah "group" yang akan diekstrak.
    pattern = r"Region=(\w+); Role=([\w\s]+); Activation=([0-9.]+)"
    
    try:
        results = re.findall(pattern, log_text)
        if not results:
            raise ValueError("Log tidak memiliki format yang valid atau kosong.")
        
        parsed_data = []
        for name, role, act_str in results:
            try:
                # Mengubah string aktivasi menjadi float.
                # Ini penting karena regex menangkapnya sebagai string.
                parsed_data.append((name, role, float(act_str)))
            except ValueError:
                # Menangani kasus di mana nilai aktivasi bukan angka yang valid.
                print(f"Peringatan: Nilai aktivasi '{act_str}' tidak valid untuk region {name}. Dilewati.")
        return parsed_data
    except Exception as e:
        # Menangani error umum selama proses parsing.
        print(f"Parsing gagal: {e}")
        # Mengembalikan list kosong jika ada error.
        return []

def save_analysis_report(regions: list[BrainRegion], status_report: str, filename: str = "stress_analysis.txt"):
    """Menyimpan laporan analisis ke dalam file teks."""
    try:
        with open(filename, "w") as file:
            file.write("--- Laporan Aktivasi Otak ---\n")
            for r in regions:
                file.write(r.get_info() + "\n")
            file.write("\n" + status_report + "\n")
        print(f"Hasil analisis disimpan ke '{filename}'")
    except IOError as error1:
        print(f"Gagal menyimpan laporan ke file '{filename}': {error1}")
    except Exception as e:
        print(f"Terjadi error tidak terduga saat menyimpan laporan: {e}")
