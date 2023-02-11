import { DjangoCSRFInterceptor } from './django-csrfinterceptor';

describe('DjangoCSRFInterceptor', () => {
  it('should create an instance', () => {
    expect(new DjangoCSRFInterceptor()).toBeTruthy();
  });
});
