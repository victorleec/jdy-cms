import uvicorn


def main():
    uvicorn.run("src.app:app", host="0.0.0.0", port=9034, reload=True)


if __name__ == "__main__":
    main()
