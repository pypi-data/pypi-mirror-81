from pathlib import Path

import thoipapy
from thoipapy import run_THOIPA_prediction
from thoipapy.predict import get_md5_checksum


def test_standalone_prediction():
    protein_name = "ERBB3"
    TMD_seq = "MALTVIAGLVVIFMMLGGTFL"
    full_seq = "MVQNECRPCHENCTQGCKGPELQDCLGQTLVLIGKTHLTMALTVIAGLVVIFMMLGGTFLYWRGRRIQNKRAMRRYLERGESIEPLDPSEKANKVLA"
    md5 = get_md5_checksum(TMD_seq, full_seq)
    thoipapy_module_path = Path(thoipapy.__file__).parent
    out_dir = thoipapy_module_path / "test/test_outputs/test_predict"

    run_THOIPA_prediction(protein_name, md5, TMD_seq, full_seq, out_dir, create_heatmap=True)

    assert (out_dir / "datafiles").is_dir()
    assert (out_dir / "heatmap.pdf").is_file()
    assert (out_dir / "heatmap.png").is_file()
    assert (out_dir / "THOIPA_out.csv").is_file()
    assert (out_dir / "THOIPA_out.xlsx").is_file()
