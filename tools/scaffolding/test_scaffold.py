from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent


def test_created_manifest_and_no_overwrite(tmp_path):
    args=['zsh',str(HERE/'scaffold_deliverable.sh'),str(tmp_path),'DEL-01','Test','--memory']
    first=subprocess.run(args,text=True,capture_output=True,check=True)
    created=[line.split(': ',1)[1] for line in first.stdout.splitlines() if line.startswith('CREATED_PATH:')]
    assert len(created)==7
    created=[p for p in created if Path(p).is_file()]
    assert len(created)==6
    assert all(Path(p).is_file() for p in created)
    for p in created:Path(p).write_text('human content')
    second=subprocess.run(args,text=True,capture_output=True,check=True)
    assert 'CREATED_PATH:' not in second.stdout
    assert all(Path(p).read_text()=='human content' for p in created)


def test_package_rerun_and_path_boundary(tmp_path):
    args=['zsh',str(HERE/'scaffold_package.sh'),str(tmp_path),'PKG-01','Test']
    assert subprocess.run(args,text=True,capture_output=True).returncode==0
    assert 'CREATED_PATH:' not in subprocess.run(args,text=True,capture_output=True).stdout
    bad=['zsh',str(HERE/'scaffold_deliverable.sh'),str(tmp_path),'../../outside','Test']
    assert subprocess.run(bad,capture_output=True).returncode==2
