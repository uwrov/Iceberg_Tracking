def main():
    parts = [int(part) for part in input().split(",")]
    print(parts[0]+parts[1]/60+parts[2]/3600)

if __name__ == "__main__":
    raise SystemExit(main())