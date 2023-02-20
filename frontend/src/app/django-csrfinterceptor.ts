import { HttpInterceptor, HttpXsrfTokenExtractor, HttpRequest, HttpHandler, HttpEvent } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";


@Injectable()
export class DjangoCSRFInterceptor implements HttpInterceptor {
    constructor(private tokenExtractor: HttpXsrfTokenExtractor) {}

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        // let csrfToken = (
        //     document.querySelector('[name=csrfmiddlewaretoken]') as HTMLInputElement
        //   ).value;

    
        //     req = req.clone({ setHeaders: {'X-CSRFToken': csrfToken }});
        //     console.log(`HTTP: Adding CSRF`);

        return next.handle(req);
    }
}
