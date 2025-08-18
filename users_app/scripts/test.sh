check_coverage () {
    pkg=$1
    min=$2
    profile="coverage.out"

    echo "==> Testing $pkg"
    go test -coverprofile=$profile -coverpkg=./... $pkg > test_output.txt
    cat test_output.txt

    # Extract total coverage percentage
    coverage=$(go tool cover -func=$profile | grep total: | awk '{print substr($3, 1, length($3)-1)}')

    echo "Coverage for $pkg: $coverage%"
    cov_int=${coverage%.*}

    if [ "$cov_int" -lt "$min" ]; then
        echo "❌ Coverage for $pkg is below $min%"
        exit 1
    else
        echo "✅ Coverage for $pkg is above $min%"
    fi

    rm test_output.txt
    rm $profile
}

check_coverage ./internal/adapter/handler/http/ 70
check_coverage ./internal/core/service/ 70
check_coverage ./internal/adapter/data/postgres/repository/ 70
