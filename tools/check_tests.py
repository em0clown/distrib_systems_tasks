import subprocess
import sys
import os

DEFAULT_GROUPS = ["431", "531", "532"]


def check_group(group: str, sid: str, start_week: int = 1, end_week: int = 17):
    print(f"\nChecking tests for {group}/{sid}...")
    for i in range(start_week, end_week + 1):
        week = str(i).zfill(2)
        print(f"Week {week}:", end=" ", flush=True)
        try:
            cmd = [sys.executable, "-m", "pytest", f"weeks/week-{week}/tests"]
            env = {**dict(os.environ), "GROUP": group, "STUDENT_ID": sid}
            result = subprocess.run(cmd, capture_output=True, env=env)
            
            if result.returncode == 0:
                print("PASS")
            elif result.returncode == 1:
                print("FAIL (Assertions failed, OK)")
            else:
                print(f"CRASH (code {result.returncode})")
                # print(result.stderr.decode()) # Uncomment for debug
        except Exception as e:
            print(f"ERROR: {e}")


def main():
    sid = os.getenv("STUDENT_ID", "s01")
    start_week = int(os.getenv("START_WEEK", "1"))
    end_week = int(os.getenv("END_WEEK", "17"))

    if len(sys.argv) > 1:
        groups = sys.argv[1:]
    elif "GROUP" in os.environ:
        groups = [os.environ["GROUP"]]
    else:
        groups = DEFAULT_GROUPS

    for group in groups:
        check_group(group, sid, start_week=start_week, end_week=end_week)


if __name__ == "__main__":
    main()
