from typing import Annotated
from fastapi import Depends, Header, HTTPException, status


def get_current_account_id(
    account_id: Annotated[str | None, Header(alias="Framedesk-Account-ID")] = None,
) -> str:
    if not account_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Framedesk-Account-ID header is missing or invalid",
        )
    return account_id


# Dependency alias for route use
CurrentAccountIdDep = Annotated[str, Depends(get_current_account_id)]
